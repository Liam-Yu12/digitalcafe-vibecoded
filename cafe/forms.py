from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import MenuItem


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ("name", "description", "price", "photo", "is_available", "display_order")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=99)
