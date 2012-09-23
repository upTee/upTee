from captcha.fields import CaptchaField

class Html5CaptchaField(CaptchaField):

    def __init__(self, *args, **kwargs):
        super(Html5CaptchaField, self).__init__(*args, **kwargs)
        required = kwargs.get('required', None)
        if required:
            self.widget.widgets[1].attrs['required'] = None
