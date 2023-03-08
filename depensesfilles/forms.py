from django import forms
from django.forms import ModelForm
from .models import Depenses, DepenseStatus, Categorie

from datetime import datetime as dt

from bootstrap_datepicker_plus.widgets import DatePickerInput

class DepensesModelForm(ModelForm):
    class Meta:
        model = Depenses
        fields="__all__"
        widgets = {'date': DatePickerInput()}