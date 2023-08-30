from collections import defaultdict
from datetime import date

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, FormView, ListView, TemplateView, DeleteView)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from shopping_list_app.forms import (
    UserLoginForm, RecipeForm, IngredientFormset, IngredientUpdateFormset, IndependentIngredientForm, ShoppingListForm)
from shopping_list_app.models import (
    ShoppingList, Recipe, Ingredient, IndependentIngredient)


def index(request):
    """View function for home page"""
    if request.user.is_authenticated:
        user = request.user
        no_of_shopping_lists = ShoppingList.objects.filter(user=user).count()
        no_of_recipes = Recipe.objects.filter(user=user).count()
        no_of_ingredients = Ingredient.objects.count()
        return render(request, 'home.html', {'user': user,
                                             'no_of_shopping_lists': no_of_shopping_lists,
                                             'no_of_recipes': no_of_recipes,
                                             'no_of_ingredients': no_of_ingredients})
    return render(request, 'base.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/register.html'

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserLoginFormView(FormView):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class RecipeListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        recipes = Recipe.objects.filter(user=user).order_by('name')
        return render(request, 'recipe_list.html', {'recipes': recipes,
                                                    'user': user})


class RecipeCreateView(LoginRequiredMixin, TemplateView):
    model = Recipe
    template_name = 'recipe_create.html'
    form_class = RecipeForm
    success_url = None
    login_url = '/login/'

    def get(self, *args, **kwargs):
        form = RecipeForm()
        formset = IngredientFormset(queryset=Recipe.objects.none())
        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})

    def post(self, request):
        form = RecipeForm(request.POST or None)
        formset = IngredientFormset(request.POST or None)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            ingredients = formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            return redirect(reverse_lazy('recipe-list'))

        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})


class RecipeDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.delete()
        return redirect('recipe-list')


class RecipeDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        ingredients = recipe.ingredients.all()
        return render(request, 'recipe_details.html', {'recipe': recipe,
                                                    'ingredients': ingredients})


class RecipeUpdateView(LoginRequiredMixin, TemplateView):
    model = Recipe
    template_name = 'recipe_update.html'
    form_class = RecipeForm
    success_url = None
    login_url = '/login/'

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id, user=request.user)
        form = RecipeForm(instance=recipe)
        formset = IngredientUpdateFormset(instance=recipe)
        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id, user=request.user)
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientUpdateFormset(request.POST, instance=recipe)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            for ingredient_form in formset.deleted_forms:
                ingredient_form.instance.delete()

            ingredients = formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            return redirect(reverse_lazy('recipe-details', kwargs={'recipe_id': recipe_id}))

        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})


class IndependentIngredientCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = IndependentIngredientForm
    template_name = 'ingredient_create.html'

    def get_success_url(self):
        return reverse_lazy('ingredient-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj = form.save()
        self.object = obj

        return HttpResponseRedirect(self.get_success_url())


class IndependentIngredientListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = 'next'

    def get(self, request):
        user = self.request.user
        independent_ingredients = IndependentIngredient.objects.filter(user=user).order_by('name')
        return render(request, 'ingredient_list.html', {'ingredients': independent_ingredients,
                                                    'user': user})


class IndependentIngredientDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, ingredient_id):
        ingredient = IndependentIngredient.objects.get(id=ingredient_id)
        ingredient.delete()
        return redirect('ingredient-list')


class IndependentIngredientUpdateView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'ingredient_update.html'
    form_class = IndependentIngredientForm

    def get(self, request, ingredient_id):
        ingredient = IndependentIngredient.objects.get(id=ingredient_id, user=request.user)
        form = IndependentIngredientForm(instance=ingredient)
        return self.render_to_response({'form': form})

    def post(self, request, ingredient_id):
        ingredient = IndependentIngredient.objects.get(id=ingredient_id, user=request.user)
        form = IndependentIngredientForm(request.POST, instance=ingredient)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = self.request.user
            ingredient.save()

            return redirect(reverse_lazy('ingredient-list'))

        return self.render_to_response({'form': form})


class ShoppingListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user = self.request.user
        shopping_lists = ShoppingList.objects.filter(user=user).order_by('creation_date')
        return render(request, 'shopping_list_list.html', {'shopping_lists': shopping_lists,
                                                    'user': user})


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = ShoppingListForm
    template_name = 'shopping_list_create.html'

    def get_success_url(self):
        return reverse_lazy('shoppinglist-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.creation_date = date.today()
        obj = form.save()
        self.object = obj

        return HttpResponseRedirect(self.get_success_url())


class ShopingListDetails(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'shopping_list_details.html'

    def get(self, request, shopping_list_id):
        shopping_list = ShoppingList.objects.get(id=shopping_list_id)
        recipes = shopping_list.recipes.all()
        recipes_ingredients_dict = defaultdict(lambda: {'quantity': 0, 'category': None})
        independent_ingredients = shopping_list.independent_ingredients.all().order_by('category')

        for recipe in recipes:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                entry = recipes_ingredients_dict[ingredient.name]
                entry['quantity'] += ingredient.quantity
                entry['category'] = ingredient.category

        summarized_recipes_ingredients = [Ingredient(name=name, quantity=info['quantity'], category=info['category'])
                                  for name, info in recipes_ingredients_dict.items()]
        summarized_recipes_ingredients.sort(key=lambda x: x.category)

        return render(request, 'shopping_list_details.html', {'shopping_list': shopping_list,
                                                    'ingredient_list': summarized_recipes_ingredients,
                                                    'independent_ingredients': independent_ingredients})


class ShoppingListDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, shopping_list_id):
        shopping_list = ShoppingList.objects.get(id=shopping_list_id)
        shopping_list.delete()
        return redirect('shoppinglist-list')


