from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

from shopping_list_app.models import Recipe, Ingredient


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Username"
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': "Password"
        }
    ))


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['user', 'ingredients']


IngredientFormset = modelformset_factory(Ingredient, fields=(
    "name", "quantity", 'unit', 'category'), extra=1)
