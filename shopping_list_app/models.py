from django.db import models
from django.contrib.auth.models import User, AbstractUser

UNITS = (
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('ml', 'mililitr'),
    ('l', 'litr'),
    ('szt.', 'sztuka'),
    ('łyżeczka', 'łyżeczka'),
    ('łyżka', 'łyżka'),
    ('szcz.', 'szczypta')
)


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.FloatField()
    unit = models.CharField(choices=UNITS, default='g', max_length=32)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(blank=True, null=True, max_length=300)
    link = models.CharField(max_length=300, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    portions = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    creation_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

