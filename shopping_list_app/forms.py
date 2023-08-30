from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory, DateField

from recipe_based_shopping_list import settings
from shopping_list_app.models import Recipe, Ingredient, IndependentIngredient, ShoppingList


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

IngredientUpdateFormset = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=['name', 'quantity', 'unit', 'category'], extra=0, can_delete=True)


class IndependentIngredientForm(forms.ModelForm):

    class Meta:
        model = IndependentIngredient
        exclude = ('user', )


class ShoppingListForm(forms.ModelForm):

    class Meta:
        model = ShoppingList
        fields = ['name', 'recipes']

    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'horizontal-checkbox-list'})
    )

