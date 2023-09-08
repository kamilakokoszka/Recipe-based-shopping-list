import pytest

from django.template.response import TemplateResponse
from django.urls import reverse

from shopping_list_app.models import (
    Recipe,
    Ingredient,
    IndependentIngredient,
    ShoppingList
)


# ---------- Recipe views tests ---------- #
@pytest.mark.django_db
def test_recipe_list(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    response = client.get(reverse('recipe-list'))
    recipes = response.context_data['recipes']

    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    assert Recipe.objects.count() == len(recipes)


@pytest.mark.django_db
def test_recipe_create(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipes_before = Recipe.objects.count()
    ingredients_before = Ingredient.objects.count()
    last_recipe_id = Recipe.objects.last().id

    assert recipes_before > 0
    assert ingredients_before > 0

    data = {
        'name': 'Recipe x',
        'description': 'abc',
        'link': 'https://recipe.com',
        'portions': 4,
        'user': user.id,
        'ingredients-TOTAL_FORMS': 2,
        'ingredients-INITIAL_FORMS': 0,
        'ingredients-MIN_NUM_FORMS': 0,
        'ingredients-MAX_NUM_FORMS': 1000,
        'ingredients-0-name': 'avocado',
        'ingredients-0-quantity': 1,
        'ingredients-0-unit': 'pc',
        'ingredients-0-category': 'fruits',
        'ingredients-0-id': (last_recipe_id + 1),
        'ingredients-1-name': 'lettuce',
        'ingredients-1-quantity': 1,
        'ingredients-1-unit': 'pc',
        'ingredients-1-category': 'vegetables',
        'ingredients-1-id': (last_recipe_id + 1)
    }

    response = client.post(reverse('recipe-create'), data)

    assert response.status_code == 302
    assert Recipe.objects.count() == recipes_before + 1
    assert Ingredient.objects.count() == ingredients_before + 2

    new_recipe = Recipe.objects.last()
    recipe_ingredients = new_recipe.ingredients.all()

    assert Recipe.objects.last().name == 'Recipe x'
    assert recipe_ingredients[0].name == 'avocado'
    assert recipe_ingredients[1].name == 'lettuce'


@pytest.mark.django_db
def test_recipe_details(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()
    response = client.get(reverse('recipe-details', args=[recipe.id]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_delete(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()

    assert Recipe.objects.filter(id=recipe.id).exists()

    response = client.post(reverse('recipe-delete', args=[recipe.id]))

    assert response.status_code == 302
    assert not Recipe.objects.filter(id=recipe.id).exists()


@pytest.mark.django_db
def test_recipe_update(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()
    existing_ingredients = recipe.ingredients.all()

    assert existing_ingredients.count() > 0

    data = {'name': 'Spaghetti',
            'description': 'xyz',
            'link': 'https://spaghetti.com',
            'portions': 10,
            'user': user.id
            }

    updated_ingredients_data = [
        {'id': ingredient.id,
         'name': 'pepper',
         'quantity': 500,
         'unit': 'g',
         'category': 'vegetables'}
        for ingredient in existing_ingredients
    ]

    data['ingredients-TOTAL_FORMS'] = len(updated_ingredients_data)
    data['ingredients-INITIAL_FORMS'] = len(updated_ingredients_data)

    for index, ingredient_data in enumerate(updated_ingredients_data):
        for key, value in ingredient_data.items():
            data[f'ingredients-{index}-{key}'] = value

    response = client.post(reverse('recipe-update', args=[recipe.id]), data)

    assert response.status_code == 302

    recipe.refresh_from_db()

    assert recipe.name == 'Spaghetti'
    assert recipe.portions == 10

    updated_ingredients = Ingredient.objects.filter(recipe=recipe)

    assert updated_ingredients[0].name == 'pepper'
    assert updated_ingredients[0].quantity == 500


# ---------- Independent ingredient views tests ---------- #
@pytest.mark.django_db
def test_ingredient_list(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    response = client.get(reverse('ingredient-list'))
    ingredients = response.context_data['ingredients']

    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    assert IndependentIngredient.objects.count() == len(ingredients)


@pytest.mark.django_db
def test_ingredient_create(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    ingredients_before = IndependentIngredient.objects.count()

    assert ingredients_before > 0

    data = {
        'name': 'olive oil',
        'quantity': 1,
        'unit': 'btl',
        'category': 'oils and sauces',
        'user': user.id
    }

    response = client.post(reverse('ingredient-create'), data)

    assert response.status_code == 302
    assert IndependentIngredient.objects.count() == ingredients_before + 1
    assert IndependentIngredient.objects.last().name == 'olive oil'


@pytest.mark.django_db
def test_ingredient_delete(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    ingredient = IndependentIngredient.objects.first()

    assert IndependentIngredient.objects.filter(id=ingredient.id).exists()

    response = client.post(reverse('ingredient-delete', args=[ingredient.id]))

    assert response.status_code == 302
    assert not IndependentIngredient.objects.filter(id=ingredient.id).exists()


@pytest.mark.django_db
def teste_ingredient_update(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    ingredient = IndependentIngredient.objects.first()

    data = {
        'name': 'sunflower oil',
        'quantity': 2,
        'unit': 'btl',
        'category': 'oils and sauces',
        'user': user.id
    }

    response = client.post(reverse('ingredient-update',
                                   args=[ingredient.id]), data)

    assert response.status_code == 302

    ingredient.refresh_from_db()

    assert ingredient.name == 'sunflower oil'
    assert ingredient.quantity == 2


# ---------- Shopping list views tests ---------- #
@pytest.mark.django_db
def test_shopping_list_list(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    response = client.get(reverse('shoppinglist-list'))
    shopping_lists = response.context_data['shopping_lists']

    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    assert ShoppingList.objects.count() == len(shopping_lists)


@pytest.mark.django_db
def test_shopping_list_create(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    shopping_lists_before = ShoppingList.objects.count()

    assert shopping_lists_before > 0

    data = {
        'name': 'Birthday party',
        'recipes': ['Recipe 1', 'Recipe 2'],
        'independent_ingredients': 'butter',
        'creation_date': '2023-09-09',
        'user': user.id
    }

    response = client.post(reverse('shoppinglist-create'), data)

    assert response.status_code == 302
    assert ShoppingList.objects.count() == shopping_lists_before + 1

    shopping_list = ShoppingList.objects.get(name='Birthday party')

    assert shopping_list.recipes.count() == 2
    assert shopping_list.independent_ingredients.count() == 1


@pytest.mark.django_db
def test_shopping_list_details(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    shopping_list = ShoppingList.objects.first()
    response = client.get(reverse('shoppinglist-details',
                                  args=[shopping_list.id]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_shopping_list_delete(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    shopping_list = ShoppingList.objects.first()

    assert ShoppingList.objects.filter(id=shopping_list.id).exists()

    response = client.post(reverse('shoppinglist-delete',
                                   args=[shopping_list.id]))

    assert response.status_code == 302
    assert not ShoppingList.objects.filter(id=shopping_list.id).exists()
