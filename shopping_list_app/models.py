from django.db import models
from django.contrib.auth.models import User


UNITS = [
    ('kg', 'kilogram'),
    ('g', 'gram'),
    ('ml', 'mililitr'),
    ('szt.', 'sztuka'),
    ('łyżka', 'łyżka'),
    ('łyżeczka', 'łyżeczka'),
    ('szcz.', 'szczypta')
]


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    unit = models.CharField(choices=UNITS)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(null=True)
    link = models.CharField(max_length=300, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    portions = models.SmallIntegerField()

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    creation_date = models.DateField()
