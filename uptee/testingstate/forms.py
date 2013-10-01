from django import forms
from testingstate.models import TestingKey


class TestingForm(forms.Form):
    key = forms.CharField(label="Testing key")

    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        self.testing_key = None

    def clean_key(self):
        key = self.cleaned_data['key']
        try:
            self.testing_key = TestingKey.objects.get(key=key)
        except TestingKey.DoesNotExist:
            raise forms.ValidationError("Wrong key!")
        if self.testing_key.is_used:
            raise forms.ValidationError("That key has been used already!")
        return key

    def save(self):
        self.testing_key.is_used = True
        self.testing_key.save()


class MoreKeysForm(forms.Form):
    keys_num = forms.IntegerField(label="Number of keys to generate", min_value=1, max_value=10)

    def __init__(self, *args, **kwargs):
        super(MoreKeysForm, self).__init__(*args, **kwargs)
        self.new_keys = []

    def save(self):
        n = self.cleaned_data.get('keys_num')
        while n:
            k = TestingKey.objects.create()
            self.new_keys.append(k.key)
            n -= 1
