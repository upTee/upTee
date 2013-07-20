from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from settings import AVAILABLE_TEMPLATES, DEFAULT_TEMPLATE
from mod.models import Mod, Option, Server, Tune


def get_template(request):
    if not request.user.is_authenticated():
        return DEFAULT_TEMPLATE
    template = request.user.profile.template
    if template not in [template_[0] for template_ in AVAILABLE_TEMPLATES if template_[2] or request.user.is_staff]:
        template = DEFAULT_TEMPLATE
        request.user.profile.template = template
        request.user.profile.save()
    return template


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    template = models.CharField(max_length=100, default=DEFAULT_TEMPLATE)
    allowed_mods = models.ManyToManyField(Mod, related_name='users')

    def active_servers(self):
        return self.user.servers.filter(is_active=True)

    def online_servers(self):
        return self.user.servers.filter(is_active=True, online=True)

    def active_count(self):
        return len(self.user.servers.filter(is_active=True))

    def online_count(self):
        return len(self.user.servers.filter(is_active=True, online=True))

    def __unicode__(self):
        possessive = '' if self.user.username.endswith('s') else 's'
        return u"{0}'{1} profile".format(self.user.username, possessive)


class Moderator(models.Model):
    server = models.ForeignKey(Server, related_name='moderators')
    user = models.ForeignKey(User, related_name='moderators')
    restart_allowed = models.BooleanField(default=False)
    edit_automatic_restart_allowed = models.BooleanField(default=False)
    edit_map_download_allowed = models.BooleanField(default=False)
    edit_votes_allowed = models.BooleanField(default=False)
    map_upload_allowed = models.BooleanField(default=False)
    console_allowed = models.BooleanField(default=False)
    edit_rcon_commands_allowed = models.BooleanField(default=False)
    allowed_options = models.ManyToManyField(Option, related_name='moderators')
    allowed_tunings = models.ManyToManyField(Tune, related_name='moderators')


class Activation(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='activation')
    key = models.CharField(max_length=32, unique=True, null=True)


def post_user_save(instance, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=instance)
        profile.save()


post_save.connect(post_user_save, sender=User, dispatch_uid='accounts.models')
