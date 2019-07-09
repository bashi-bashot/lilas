from django import forms
from django.contrib.admin import widgets


class UploadFileForm(forms.Form):
    fileConf = forms.FileField(required=False)
    fileSyst = forms.FileField(required=False)
    fileOpe = forms.FileField(required=False)
    fileCom = forms.FileField(required=False)
    fileInc = forms.FileField(required=False)