from datetime import date
import os
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from fields import Html5CaptchaField
from html5input import *
from settings import AVAILABLE_TEMPLATES, TEMPLATE_DIRS
from accounts.models import UserProfile


class SettingsUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=Html5EmailInput(attrs={'required': None}))

    class Meta:
        model = User
        fields = ('first_name', 'email')


class SettingsUserprofileForm(forms.ModelForm):
    template_choices = [(template_[0], template_[1]) for template_ in AVAILABLE_TEMPLATES]
    template = forms.ChoiceField(choices=template_choices)

    BOOL_CHOICES = (
        (True, 'Show to everyone'),
        (False, 'Show only to registered users'),
    )

    def __init__(self, *args, **kwargs):
        super(SettingsUserprofileForm, self).__init__(*args, **kwargs)
        if not self.instance.user.is_staff:
            self.fields['template'].choices = [(template_[0], template_[1]) for template_ in AVAILABLE_TEMPLATES if template_[2] or template_[0] == self.instance.template]
        self.initial['template'] = self.instance.template

    class Meta:
        model = UserProfile
        fields = ('publish_name', 'ingame_name', 'publish_ingame_name', 'website', 'publish_website', 'contact', 'publish_contact', 'fav_mod', 'publish_fav_mod', 'fav_map', 'publish_fav_map', 'gender', 'publish_gender', 'birthday', 'publish_birthday', 'template')
        widgets = {
            'publish_name': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_ingame_name': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_website': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_contact': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_fav_mod': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_fav_map': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'publish_gender': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
            'birthday': Html5SelectDateWidget(years=range(1930, timezone.now().year)),
            'publish_birthday': forms.Select(choices=((True, 'Show to everyone'), (False, 'Show only to registered users'))),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday and birthday > date.today():
            raise forms.ValidationError('You cannot be born in the future.')
        return birthday

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
        old_password = self.cleaned_data['old_password']
        if not self.current_user.check_password(old_password):
            raise forms.ValidationError('Please enter your current password correctly.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        if new_password1 != new_password2:
            raise forms.ValidationError("The password doesn't match the other.")
        return new_password2

    def save(self):
        self.current_user.set_password(self.cleaned_data['new_password1'])
        self.current_user.save()


class RecoverPasswordForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'required': None}))
    captcha = Html5CaptchaField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(is_active=True, username=username)
        if not user:
            raise forms.ValidationError("No user with this name exists.")
        return username


class RecoverUsernameForm(forms.Form):
    email = forms.EmailField(label='email', widget=Html5EmailInput(attrs={'required': None}))
    captcha = Html5CaptchaField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(is_active=True, email=email)
        if not user:
            raise forms.ValidationError("No user with this email exists.")
        return email


class RegisterForm(forms.Form):
    username = forms.RegexField(label="Username", min_length=3, regex=r'^[\w.@+-]+$',
        error_messages={'invalid': 'Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters.'},
        widget=forms.TextInput(attrs={'pattern': r'[\w.@+-]{3,30}', 'title': '30 characters or fewer. Letters, numbers and @/./+/-/_ characters', 'required': None, 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None, 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password again', min_length=8,
        widget=forms.PasswordInput(render_value=False, attrs={'pattern': r'.{8,}', 'title': '8 characters are required', 'required': None, 'placeholder': 'Password again'}))
    email = forms.EmailField(required=True, widget=Html5EmailInput(attrs={'required': None, 'placeholder': 'Email'}))
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
