from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.forms import inlineformset_factory

from shopping_list_app.models import (Recipe, Ingredient, IndependentIngredient, ShoppingList)


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
        fields = ['name', 'description', 'link', 'portions']


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'category']


IngredientFormset = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=['name', 'quantity', 'unit', 'category'], extra=1, can_delete=False)

IngredientUpdateFormset = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=['name', 'quantity', 'unit', 'category'], extra=0, can_delete=True)


class IndependentIngredientForm(forms.ModelForm):

    class Meta:
        model = IndependentIngredient
        fields = ['name', 'quantity', 'unit', 'category']


class ShoppingListForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['name', 'recipes', 'independent_ingredients']

    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'horizontal-checkbox-list'})
    )

    independent_ingredients = forms.ModelMultipleChoiceField(
        queryset=IndependentIngredient.objects.all(),
        to_field_name='name',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'horizontal-checkbox-list'}),
    )
