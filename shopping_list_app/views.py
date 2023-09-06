from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, FormView, ListView, TemplateView, DeleteView)

from collections import defaultdict
from datetime import date

from shopping_list_app.models import (ShoppingList, Recipe, Ingredient, IndependentIngredient)
from shopping_list_app.forms import (
    UserLoginForm,
    RecipeForm,
    IngredientFormset,
    IngredientUpdateFormset,
    IndependentIngredientForm,
    ShoppingListForm)


def index(request):
    """View function for home page"""
    if request.user.is_authenticated:
        user = request.user
        no_of_shopping_lists = ShoppingList.objects.filter(user=user).count()
        no_of_recipes = Recipe.objects.filter(user=user).count()
        no_of_ingredients = IndependentIngredient.objects.count()
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
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginFormView(FormView):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home-page')


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    login_url = "/login/"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(RecipeListView, self).get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(user=self.request.user).order_by('name')
        return context


class RecipeCreateView(LoginRequiredMixin, View):
    template_name = 'recipe/recipe_create.html'
    success_url = reverse_lazy('recipe-list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = RecipeForm()
        formset = IngredientFormset(queryset=Recipe.objects.none())
        return render(request, self.template_name, {'form': form,
                                                    'ingredient_formset': formset})

    def post(self, request):
        form = RecipeForm(request.POST)
        formset = IngredientFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()

            ingredients = formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form,
                                                    'ingredient_formset': formset})


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipe-list')
    login_url = '/login/'
    redirect_field_name = 'next'


class RecipeDetailsView(LoginRequiredMixin, View):
    template_name = 'recipe/recipe_details.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        ingredients = recipe.ingredients.all()
        return render(request, self.template_name, {'recipe': recipe,
                                                    'ingredients': ingredients})


class RecipeUpdateView(LoginRequiredMixin, View):
    template_name = 'recipe/recipe_update.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id, user=request.user)
        form = RecipeForm(instance=recipe)
        formset = IngredientUpdateFormset(instance=recipe)
        return render(request, self.template_name, {'form': form,
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

        return render(request, self.template_name, {'form': form,
                                                    'ingredient_formset': formset})


class IndependentIngredientListView(LoginRequiredMixin, ListView):
    model = IndependentIngredient
    template_name = 'ingredient/ingredient_list.html'
    login_url = "/login/"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(IndependentIngredientListView, self).get_context_data(**kwargs)
        context['ingredients'] = IndependentIngredient.objects.filter(user=self.request.user).order_by('category')
        return context


class IndependentIngredientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ingredient/ingredient_create.html'
    form_class = IndependentIngredientForm
    success_url = reverse_lazy('ingredient-list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj = form.save()
        self.object = obj

        return redirect(self.success_url)


class IndependentIngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = IndependentIngredient
    context_object_name = 'ingredient'
    success_url = reverse_lazy('ingredient-list')
    login_url = '/login/'
    redirect_field_name = 'next'


class IndependentIngredientUpdateView(LoginRequiredMixin, View):
    template_name = 'ingredient/ingredient_update.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, ingredient_id):
        ingredient = IndependentIngredient.objects.get(id=ingredient_id, user=request.user)
        form = IndependentIngredientForm(instance=ingredient)
        return render(request, self.template_name, {'form': form})

    def post(self, request, ingredient_id):
        ingredient = IndependentIngredient.objects.get(id=ingredient_id, user=request.user)
        form = IndependentIngredientForm(request.POST, instance=ingredient)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = self.request.user
            ingredient.save()

            return redirect(reverse_lazy('ingredient-list'))

        return render(request, self.template_name, {'form': form})


class ShoppingListView(LoginRequiredMixin, TemplateView):
    model = ShoppingList
    template_name = 'shopping_list/shopping_list_list.html'
    login_url = "/login/"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(ShoppingListView, self).get_context_data(**kwargs)
        context['shopping_lists'] = ShoppingList.objects.filter(user=self.request.user).order_by('-creation_date')
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    form_class = ShoppingListForm
    template_name = 'shopping_list/shopping_list_create.html'
    success_url = reverse_lazy('shoppinglist-list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.creation_date = date.today()
        obj = form.save()
        self.object = obj

        return redirect(self.success_url)


class ShoppingListDeleteView(LoginRequiredMixin, DeleteView):
    model = ShoppingList
    context_object_name = 'shopping_list'
    success_url = reverse_lazy('shoppinglist-list')
    login_url = '/login/'
    redirect_field_name = 'next'


class ShoppingListDetails(LoginRequiredMixin, View):
    template_name = 'shopping_list/shopping_list_details.html'
    login_url = '/login/'
    redirect_field_name = 'next'

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

        return render(request, self.template_name, {'shopping_list': shopping_list,
                                                    'ingredient_list': summarized_recipes_ingredients,
                                                    'independent_ingredients': independent_ingredients})
