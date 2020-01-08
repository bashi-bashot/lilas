from django import forms
from django.contrib.admin import widgets
from .exception import *


class UploadFileForm(forms.Form):
    fileConf = forms.FileField(required=False)

    fileSyst = forms.FileField(required=False)

    fileOpe = forms.FileField(required=False)
    
    fileCom = forms.FileField(required=False)

    fileInc = forms.FileField(required=False)

    # def clean_fileOpeError(self):
    #     data = self.cleaned_data['fileOpeError']
    #     print(data)
    #     if "Le Format attendu est un fichier CSV" in data:
    #         raise forms.ValidationError(data, code="invalid format")
    #     return data