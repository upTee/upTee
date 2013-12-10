from captcha.conf import settings as captcha_settings
from captcha.models import CaptchaStore
from django import template

register = template.Library()


class CaptchaNode(template.Node):
    def __init__(self):
        challenge, response = captcha_settings.get_challenge()()
        store = CaptchaStore.objects.create(challenge=challenge, response=response)
        self.key = store.hashkey

    def render(self, context):
        context['captcha_key'] = self.key
        return ''


@register.tag
def captcha_tag(parser, token):
    return CaptchaNode()
