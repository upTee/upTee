import mimetypes
import os
import tarfile
import zipfile
from django import forms
from mod.models import Mod, Server


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
