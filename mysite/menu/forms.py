from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient
import datetime
from django.forms import ValidationError


class MenuForm(forms.ModelForm):

    expiration_date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%m/%d/%Y'),
        input_formats=['%m/%d/%Y'], error_messages={'invalid': 'Invalid date use format: MM/DD/YYYY'}, required=False)

    class Meta:
        model = Menu
        exclude = ('created_date',)
