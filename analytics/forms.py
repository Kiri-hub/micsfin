from importlib.metadata import requires
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.forms import ModelForm
from .models import Student, Professor


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ["name", "surname", "picture"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "picture": forms.FileInput(attrs={"class": "form-control"}),
        }