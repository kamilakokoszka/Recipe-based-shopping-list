from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from shopping_list_app.forms import UserLoginForm, RecipeForm, IngredientFormset
from shopping_list_app.models import ShoppingList, Recipe, Ingredient, Category


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
    template_name = 'add_recipe.html'
    login_url = '/login/'

    def get(self, *args, **kwargs):
        form = RecipeForm()
        formset = IngredientFormset(queryset=Ingredient.objects.none())
        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})

    def post(self, *args, **kwargs):
        form = RecipeForm(self.request.POST)
        formset = IngredientFormset(data=self.request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            ingredients = formset.save(commit=True)
            recipe.ingredients.set(ingredients)

            return redirect(reverse_lazy('recipe-list'))

        return self.render_to_response({'form': form,
                                        'ingredient_formset': formset})