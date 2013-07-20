import os
from django.contrib.auth.models import User
from django import forms
from fields import Html5CaptchaField
from html5input import *
from settings import AVAILABLE_TEMPLATES, TEMPLATE_DIRS


class SettingsUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=Html5EmailInput(attrs={'required': None}))

    template_choices = [(template_[0], template_[1]) for template_ in AVAILABLE_TEMPLATES]
    template = forms.ChoiceField(choices=template_choices)

    def __init__(self, *args, **kwargs):
        super(SettingsUserForm, self).__init__(*args, **kwargs)
        if not self.instance.is_staff:
            self.fields['template'].choices = [(template_[0], template_[1]) for template_ in AVAILABLE_TEMPLATES if template_[2] or template_[0] == self.instance.profile.template]
        self.initial['template'] = self.instance.profile.template

    class Meta:
        model = User
        fields = ('email',)

    def clean_template(self):
        template = self.cleaned_data['template']
        found = False
        for path in TEMPLATE_DIRS:
            if os.path.exists(os.path.join(path, template)):
                found = True
                break
        if not found:
            raise forms.ValidationError('Template does not exist. Please contact an admin.')
        return template

    def save(self):
        if self.instance.profile.template != self.cleaned_data['template']:
            self.instance.profile.template = self.cleaned_data['template']
            self.instance.profile.save()
        super(SettingsUserForm, self).save()


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Old password',
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None}))
    new_password1 = forms.CharField(label='New password', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None}))
    new_password2 = forms.CharField(label='New password again', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None}))

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        if self.current_user is None:
            raise AttributeError('current_user missing')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.current_user.check_password(old_password):
            raise forms.ValidationError(
                'Please enter your current password correctly.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError(
                u"The password doesn't match the other.")
        return new_password2

    def save(self):
        self.current_user.set_password(self.cleaned_data.get('new_password1'))
        self.current_user.save()


class RegisterForm(forms.Form):
    username = forms.RegexField(label="Username", min_length=3, regex=r'^[\w.@+-]+$',
        error_messages={'invalid': 'Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters.'},
        widget=forms.TextInput(attrs={'pattern': r'[\w.@+-]{3,30}', 'title': '30 characters or fewer. Letters, numbers and @/./+/-/_ characters', 'required': None}))
    password1 = forms.CharField(label='Password', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None}))
    password2 = forms.CharField(label='Password again', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None}))
    email = forms.EmailField(required=True, widget=Html5EmailInput(attrs={'required': None}))
    captcha = Html5CaptchaField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if users:
            raise forms.ValidationError(
                u"A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError(
                u"A user with this email address already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(
                u"The password doesn't match the other.")
        return password2
