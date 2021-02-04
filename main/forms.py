from .models import NewUser
from django.forms import ModelForm,TypedChoiceField
from django import forms

subscription_choices = (
    ("Standart", "Standart"),
    ("VIP", "VIP"),
    ("Premium", "Premium"),
)


class UserForm(forms.Form):
    sub = forms.TypedChoiceField(
                   choices=subscription_choices,
                   coerce=str
                  )


