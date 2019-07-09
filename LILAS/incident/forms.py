from django import forms
from django.contrib.admin import widgets

class DateForm(forms.Form):
    dateDebut = forms.DateField(label='Date de début : ', widget=widgets.AdminDateWidget())
    heureDebut  = forms.CharField(label='Heure de début (xx:xx:xx)', max_length=8)
    dateFin = forms.DateField(label='Date de fin : ',  widget=widgets.AdminDateWidget())
    heureFin = forms.CharField(label='Heure de Fin (xx:xx:xx)', max_length=8)

