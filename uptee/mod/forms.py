import mimetypes
import os
import tarfile
import zipfile
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import utc
from accounts.models import Moderator
from mod.models import Mod, Server, TaskEvent


class ModAdminForm(forms.ModelForm):

    class Meta:
        model = Mod

    def clean_mod_file(self):
        mod_file = self.cleaned_data['mod_file']
        mimetype = mimetypes.guess_type(mod_file.name)[0]
        if mimetype not in ('application/zip', 'application/x-tar'):
            raise forms.ValidationError(
                u'You can only upload .zip and .tar files.')
        if mimetype == 'application/zip':
            if not zipfile._check_zipfile(mod_file.file):
                raise forms.ValidationError(
                    u'The file is no valid archieve.')
        elif mimetype == 'application/x-tar':
            try:
                t = tarfile.open(fileobj=mod_file.file)
                t.close()
            except:
                raise forms.ValidationError(
                    u'The file is no valid archieve.')
        return mod_file


class ServerAdminForm(forms.ModelForm):

    class Meta:
        model = Server
        fields = ('owner', 'mod', 'is_active')


class MapUploadForm(forms.Form):
    map_file = forms.FileField(label='Map')

    def clean_map_file(self):
        map_file = self.cleaned_data['map_file']
        if os.path.splitext(map_file.name)[1] != '.map':
            raise forms.ValidationError('The uploaded file is not a map.')
        if map_file.read(4) not in ['DATA', 'ATAD']:
            raise forms.ValidationError('The uploaded file is not a valid map file.')
        map_file.seek(os.SEEK_SET)
        return map_file


class ChangeModForm(forms.ModelForm):
    mod = forms.ModelChoiceField(Mod.objects, empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(ChangeModForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['mod'].queryset = user.profile.allowed_mods.all()

    def clean_mod(self):
        mod = self.cleaned_data['mod']
        if mod == Server.objects.get(pk=self.instance.pk).mod:
            raise forms.ValidationError('You chose the very same mod.')
        return mod

    class Meta:
        model = Server
        fields = ('mod',)

    def save(self):
        old_instance = Server.objects.get(pk=self.instance.pk)
        self.instance.reset_settings(old_instance)
        self.instance.save()


class ServerDescriptionForm(forms.ModelForm):

    class Meta:
        model = Server
        fields = ('description',)


class ModeratorForm(forms.Form):
    user = forms.ModelChoiceField(User.objects, empty_label=None)

    def __init__(self, user, server, *args, **kwargs):
        super(ModeratorForm, self).__init__(*args, **kwargs)
        self.server = server
        self.fields['user'].queryset = User.objects.exclude(pk=user.pk)
        for moderator in server.moderators.all():
            self.fields['user'].queryset = self.fields['user'].queryset.exclude(pk=moderator.user.pk)

    def save(self):
        user = self.cleaned_data['user']
        moderator = Moderator(server=self.server, user=user)
        moderator.save()


class CommandForm(forms.Form):
    command = forms.CharField(max_length=500)


class TaskEventAdminForm(forms.ModelForm):
    timezone_offset = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = TaskEvent

    def clean_date(self):
        date = self.cleaned_data['date']
        date = date.replace(tzinfo=utc)
        if date <= timezone.now():
            raise forms.ValidationError('Choose a time in the future.')
        return date

    def clean_repeat(self):
        repeat = self.cleaned_data['repeat']
        if repeat < 0:
            raise forms.ValidationError('Time has to be positive.')
        return repeat


class TaskEventForm(TaskEventAdminForm):
    date = forms.DateTimeField(help_text='MM/DD/YYYY hh:mm:ss')

    class Meta:
        model = TaskEvent
        fields = ('name', 'task_type', 'date', 'repeat')
