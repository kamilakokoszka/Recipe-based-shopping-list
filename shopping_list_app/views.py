from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return HttpResponseRedirect(self.get_success_url())

