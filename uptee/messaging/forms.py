from django import forms
from fields import Html5CaptchaField
from html5input import Html5EmailInput


class ContactForm(forms.Form):
    email = forms.EmailField(required=True, widget=Html5EmailInput(attrs={'required': None}))
    message = forms.CharField(widget=forms.Textarea(attrs={'required': None}))
    captcha = Html5CaptchaField(required=True)
