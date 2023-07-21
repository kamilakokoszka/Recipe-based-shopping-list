"""recipe_based_shopping_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shopping_list_app import views
from django.contrib.auth import views as auth_views
from shopping_list_app.forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home-page'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                authentication_form=UserLoginForm,
                                                next_page='home-page'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('add-recipe/', views.CreateRecipeView.as_view(), name='add-recipe')
]
