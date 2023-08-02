from django.db import models
from django.contrib.auth.models import User, AbstractUser

UNITS = (
    ('g', 'gram'),
    ('ml', 'milliliter'),
    ('pc', 'piece'),
    ('tsp', 'teaspoon'),
    ('tbsp', 'tablespoon'),
    ('pinch', 'pinch')
)

CATEGORIES = (
    ('bakery and bread', ' Bakery and Bread'),
    ('meat and seafood', 'Meat and Seafood'),
    ('pasta and rice', 'Pasta and Rice'),
    ('oils and sauces', 'Oils and Sauces'),
    ('dairy and eggs', 'Dairy and eggs'),
    ('fruits', 'Fruits'),
    ('vegetables', 'Vegetables'),
    ('spices', 'Spices'),
    ('other', 'Other')
)

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(blank=True, null=True, max_length=300)
    link = models.CharField(max_length=300, null=True, blank=True)
    portions = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def no_of_ingredients(self):
        return self.ingredients.count()


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.FloatField(max_length=6)
    unit = models.CharField(choices=UNITS, default='g')
    category = models.CharField(choices=CATEGORIES, default='Other')
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IndependentIngredient(Ingredient):
    pass


class ShoppingList(models.Model):
    name = models.CharField(max_length=128, default='Shopping list')
    recipes = models.ManyToManyField(Recipe)
    creation_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

