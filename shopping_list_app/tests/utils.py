from faker import Faker
from random import randint

from shopping_list_app.models import Recipe, Ingredient, IndependentIngredient, ShoppingList
from django.contrib.auth.models import User

faker = Faker("en_EN")


def create_fake_user():
    User.objects.create(username=faker.name(), password=faker.password())


def create_fake_recipes():
    create_fake_user()

    for _ in range(3):
        description = faker.paragraph(nb_sentences=1, ext_word_list=['abc', 'def', 'ghi', 'jkl'])
        Recipe.objects.create(name=f'Recipe {_}',
                              description=description,
                              link=faker.url(),
                              portions=randint(1, 4),
                              user=User.objects.first())


def create_fake_ingredients():
    create_fake_recipes()
    recipes = Recipe.objects.all()

    Ingredient.objects.create(name='tomato', quantity='2', unit='pc', category='vegetables', recipe=recipes[0])
    Ingredient.objects.create(name='apple', quantity='100', unit='g', category='fruits', recipe=recipes[1])
    Ingredient.objects.create(name='milk', quantity='200', unit='ml', category='dairy and eggs', recipe=recipes[2])
    Ingredient.objects.create(name='salt', quantity='1', unit='pinch', category='spices', recipe=recipes[randint(0, 2)])
    Ingredient.objects.create(name='water', quantity='50', unit='ml', category='other', recipe=recipes[randint(0, 2)])
    Ingredient.objects.create(name='rice', quantity='500', unit='g', category='pasta and rice',
                              recipe=recipes[randint(0, 2)])


def create_fake_independent_ingredients():
    create_fake_user()
    user = User.objects.first()
    IndependentIngredient.objects.create(name='olive oil', quantity='1', unit='btl', category='oils and sauces',
                                         user=user)
    IndependentIngredient.objects.create(name='butter', quantity='150', unit='g', category='dairy and eggs', user=user)
    IndependentIngredient.objects.create(name='watermelon', quantity='1', unit='pc', category='fruits', user=user)


def create_shopping_list():
    create_fake_user()
    create_fake_recipes()
    create_fake_independent_ingredients()
    user = User.objects.first()

    for _ in range(0, 3):
        recipes = Recipe.objects.order_by('?')
        independent_ingredients = IndependentIngredient.objects.order_by('?')
        random_recipes = recipes[0, 2]
        random_independent_ingredient = independent_ingredients[0]
        ShoppingList.objects.create(name=f'Shopping list {_}',
                                    recipes=random_recipes,
                                    independent_ingredients=random_independent_ingredient,
                                    creation_date=faker.date_this_month(),
                                    user=user)
