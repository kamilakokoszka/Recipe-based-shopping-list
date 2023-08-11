from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

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
        exclude = ['user', ]


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        exclude = ('recipe', )


IngredientFormset = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=['name', 'quantity', 'unit', 'category'], extra=1, can_delete=False)
