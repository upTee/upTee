from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from settings import DEFAULT_TEMPLATE


def get_template(request):
    return DEFAULT_TEMPLATE if not request.user.is_authenticated() else request.user.profile.template


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    template = models.CharField(max_length=100, default=DEFAULT_TEMPLATE)

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


def post_user_save(instance, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=instance)
        profile.save()


post_save.connect(post_user_save, sender=User, dispatch_uid='accounts.models')
