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


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "is_active", "professor", "students_courses", "notations"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "professor": forms.Select(attrs={"class": "form-select", "required": True}),
            "students_courses": forms.SelectMultiple(attrs={"class": "form-select", "required": True}),
            "notations": forms.Textarea(attrs={"class": "form-control"})
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )