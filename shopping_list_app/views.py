from django.contrib.auth import login
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
    UserLoginForm, RecipeForm, IngredientFormset, IngredientUpdateFormset)
from shopping_list_app.models import (
    ShoppingList, Recipe, Ingredient)


def index(request):
    """View function for home page"""
    if request.user.is_authenticated:
        user = request.user
        no_of_shopping_lists = ShoppingList.objects.filter(user=user)
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


class CreateRecipeView(LoginRequiredMixin, TemplateView):
    model = Recipe
    template_name = 'add_recipe.html'
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


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
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
        return render(request, 'recipe_view.html', {'recipe': recipe,
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
