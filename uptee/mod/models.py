import mimetypes, os, psutil, signal, tarfile, zipfile
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from mod.tasks import run_server
from shutil import move, rmtree
from settings import MEDIA_ROOT
from twconfig import Config as TwCongig

class FreePortManager(models.Manager):
    def get_query_set(self):
        return super(FreePortManager, self).get_query_set().filter(is_active=False)


class Mod(models.Model):
    mod_file = models.FileField(upload_to='uploads', help_text='Should be .zip or .tar')
    upload_date = models.DateTimeField('Uploaddatum', auto_now=True)
    title = models.CharField(blank=False, max_length=100)
    mimetype = models.CharField(editable=False, max_length=100)

    class Meta:
        ordering = ['upload_date', 'title']

    def __unicode__(self):
        return self.title

    def save(self):
        self.mimetype = mimetypes.guess_type(self.mod_file.path)[0]
        super(Mod, self).save()
        tmp_dir = os.path.join(MEDIA_ROOT, 'tmp')
        servers = Server.objects.all()
        for user in User.objects.filter(is_active=True):
            if not servers.filter(owner=user).filter(mod=self):
                continue

            mod_path = os.path.join(MEDIA_ROOT, 'users', user.username, self.title)
            map_path = os.path.join(mod_path, 'data', 'maps')
            if os.path.exists(map_path):
                move(map_path, os.path.join(tmp_dir, 'maps'))
            if os.path.exists(mod_path):
                rmtree(mod_path)
            os.makedirs(mod_path)
            if self.mimetype == 'application/zip':
                with zipfile.ZipFile(self.mod_file.path) as z:
                    z.extractall(mod_path)
            elif self.mimetype == 'application/x-tar':
                with tarfile.TarFile(mod.mod_file.path) as t:
                    t.extractall(mod_path)
            if os.path.exists(os.path.join(tmp_dir, 'maps')):
                rmtree(map_path)
                move(os.path.join(tmp_dir, 'maps'), os.path.join(mod_path, 'data'))

    def delete(self):
        if os.path.exists(self.mod_file.path):
            os.remove(self.mod_file.path)
        super(Mod, self).delete()

class Port(models.Model):
    port = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)

    objects = models.Manager()
    free = FreePortManager()

    @staticmethod
    def get_free_port():
        try:
            return Port.free.all()[0]
        except:
            return None

    class Meta:
        ordering = ['port']

    def __unicode__(self):
        return str(self.port)

    def validate_unique(self, exclude=None):
        if self.port < 0 or self.port > 65535:
            raise ValidationError('The used Port is out of range.')
        super(Port, self).validate_unique(exclude=exclude)

    def save(self):
        self.full_clean()
        super(Port, self).save()

class Server(models.Model):
    owner = models.OneToOneField(User, related_name='server')
    mod = models.ForeignKey(Mod, related_name='servers')
    pid = models.IntegerField(blank=True, null=True, unique=True)
    port = models.ForeignKey(Port, blank=True, null=True, related_name='server')
    is_active = models.BooleanField(default=False)

    @property
    def is_online(self):
        if self.port and self.port.is_active:
            return True
        return False

    def __unicode__(self):
        return '{0} ({1}) Owner: {2}'.format(self.mod.title, self.is_online, self.owner.username)

    def check_online(self):
        if self.pid in psutil.get_pid_list():
            return True
        self.set_offline()
        return False

    def set_offline(self):
        if self.port and self.port.is_active:
            self.port.is_active = False
            self.port.save()
            self.port = None
        if self.pid in psutil.get_pid_list():
            os.kill(self.pid, signal.SIGTERM)
        self.pid = None
        self.save()

    def set_online(self):
        self.port = Port.get_free_port()
        self.port.is_active = True
        self.port.save()
        path = os.path.join(MEDIA_ROOT, 'users', self.owner.username, self.mod.title)
        config = TwCongig(os.path.join(path, 'generated.cfg'))
        for option in self.config_options.all():
            config.add_option(option.command, option.value)
        config.add_option('sv_port', self.port.port)
        for tune in self.config_tunes.all():
            config.add_tune(tune.command, tune.value)
        for vote in self.config_votes.all():
            config.add_vote(vote.command, vote.title)
        config.write()
        run_server.delay(path, self)

    def delete(self):
        self.set_offline()
        path = os.path.join(MEDIA_ROOT, 'users', self.owner.username, self.mod.title)
        if os.path.exists(path):
            rmtree(path)
        super(Server, self).delete()

class Config(models.Model):
    server = models.ForeignKey(Server, related_name='config_%(class)ss')
    command = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Option(Config):
    value = models.CharField(blank=True, max_length=500)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return str(self.command)

class Tune(Config):
    value = models.FloatField()

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return str(self.command)

class Vote(Config):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return str(self.command)
    