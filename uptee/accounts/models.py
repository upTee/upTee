from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
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
    allowed_mods = models.ManyToManyField(Mod, blank=True, related_name='users')

    GENDER_NONE = 1
    GENDER_MALE = 2
    GENDER_FEMALE = 3
    GEDGET_CHOICES = (
        (GENDER_NONE, 'Not saying'),
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )
    gender = models.IntegerField(choices=GEDGET_CHOICES, default=GENDER_NONE)
    publish_gender = models.BooleanField(default=False)
    birthday = models.DateField(blank=True, null=True, help_text='only your age will be shown (e.g. 15-20) | (MM/DD/YYYY)')
    publish_birthday = models.BooleanField(default=False)
    ingame_name = models.CharField(max_length=20, blank=True, null=True, default='')
    publish_ingame_name = models.BooleanField(default=False)
    fav_map = models.CharField(max_length=50, blank=True, null=True, default='', verbose_name='favorite map')
    publish_fav_map = models.BooleanField(default=False)
    fav_mod = models.CharField(max_length=20, blank=True, null=True, default='', verbose_name='favorite mod')
    publish_fav_mod = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, blank=True, null=True, default='')
    publish_contact = models.BooleanField(default=False)
    website = models.URLField(blank=True, null=True, default='')
    publish_website = models.BooleanField(default=False)
    publish_name = models.BooleanField(default=False)

    def active_servers(self):
        return self.user.servers.filter(is_active=True)

    def online_servers(self):
        return self.user.servers.filter(is_active=True, online=True)

    def active_count(self):
        return len(self.user.servers.filter(is_active=True))

    def online_count(self):
        return len(self.user.servers.filter(is_active=True, online=True))

    @property
    def get_age(self):
        age = relativedelta(dt1=date.today(), dt2=self.birthday).years
        if age < 8:
            return '0-7'
        elif age < 13:
            return '8-12'
        elif age < 18:
            return '13-17'
        elif age < 22:
            return '18-21'
        elif age < 28:
            return '22-27'
        elif age < 38:
            return '28-37'
        elif age < 51:
            return '38-50'
        else:
            return 'near death'

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


class Activation(models.Model):  # also used for password recover
    user = models.OneToOneField(User, unique=True, related_name='activation')
    key = models.CharField(max_length=32, unique=True, null=True)


def post_user_save(instance, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=instance)
        profile.save()


post_save.connect(post_user_save, sender=User, dispatch_uid='accounts.models')
