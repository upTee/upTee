import mimetypes
import os
import tarfile
import zipfile
from django import forms
from mod.models import Mod, Option, Server, Tune, Vote
from settings import MEDIA_ROOT
from lib.twconfig import Config as TwCongig


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

    def clean_mod(self):
        mod = self.cleaned_data['mod']
        if mod == Server.objects.get(pk=self.instance.pk).mod:
            raise forms.ValidationError('You chose the very same mod.')
        return mod

    class Meta:
        model = Server
        fields = ('mod',)

    def save(self):
        for option in Option.objects.filter(server=self.instance):
            option.delete()
        for tune in Tune.objects.filter(server=self.instance):
            tune.delete()
        for vote in Vote.objects.filter(server=self.instance):
            vote.delete()
        config_path = os.path.join(MEDIA_ROOT, 'mods', self.instance.mod.title, 'config.cfg')
        config = TwCongig(config_path)
        config.read()
        for key, value in config.options.iteritems():
            widget = 1  # text
            for widget_type in Option.WIDGET_CHOICES:
                if widget_type[1] == value[1]:
                    widget = widget_type[0]
            data = Option(server=self.instance, command=key, value=value[0], widget=widget)
            data.save()
        for tune in config.tunes:
            data = Tune(server=self.instance, command=tune['command'], value=tune['value'])
            data.save()
        for vote in config.votes:
            data = Vote(server=self.instance, command=vote['command'], title=vote['title'])
            data.save()
        self.instance.save()
