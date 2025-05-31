from django import forms
from django.core import validators
from django.contrib.auth.models import User

def validateName(name):
    for char in name:
        if char.isdigit():
            raise forms.ValidationError("Card/set name can not contain any numbers.")

def validateNumber(number):
    for char in number:
        if not char.isdigit():
            raise forms.ValidationError("Card number can only contain digits 0-9.")

class SearchCardForm(forms.Form):
    card_name = forms.CharField(
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Pikachu", "style": "font-size:small"}),
        validators=[
            validators.MinLengthValidator(3),
            validators.MaxLengthValidator(50),
            validateName
        ]
    )
    set_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Base", "style": "font-size:small"}),
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(50),
            validateName
        ],
        required=False
    )
    card_number = forms.CharField(
        min_length=1,
        max_length=3,
        widget=forms.TextInput(attrs={"placeholder": "87", "style": "font-size:small"}),
        validators=[
            validators.MinLengthValidator(1),
            validators.MaxLengthValidator(3),
            validateNumber
        ]
    )

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"size": "30"}))

    class Meta():
        model = User
        fields = ("username", "email", "password")
        help_texts = {"username": None}

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())