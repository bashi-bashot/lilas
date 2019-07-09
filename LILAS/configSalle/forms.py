from django import forms
from django.contrib.admin import widgets

class DateForm(forms.Form):
    date = forms.DateField(label='dateForm', widget=widgets.AdminDateWidget())