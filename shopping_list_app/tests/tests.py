import pytest

from django.template.response import TemplateResponse
from django.urls import reverse

from shopping_list_app.tests.utils import create_fake_ingredient
from shopping_list_app.models import Recipe, Ingredient, IndependentIngredient, ShoppingList


@pytest.mark.django_db
def test_recipe_list(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    response = client.get('/recipe/list/')

    recipes = response.context_data['recipes']

    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    assert Recipe.objects.count() == len(recipes)


@pytest.mark.django_db
def test_recipe_create(client, user, set_up):
    client.login(username='Superadmin', password='123password')

    recipes_before = Recipe.objects.count()
    ingredients_before = Ingredient.objects.count()

    assert recipes_before > 0
    assert ingredients_before > 0

    create_fake_ingredient()
    new_recipe = Recipe.objects.last()

    response = client.post('/recipe/create/', data={
        'name': new_recipe.name,
        'description': new_recipe.description,
        'link': new_recipe.link,
        'portions': new_recipe.portions,
        'user': new_recipe.user.id,
    })

    assert response.status_code == 200
    assert Recipe.objects.count() == recipes_before + 1
    assert Ingredient.objects.count() == ingredients_before + 1
    assert new_recipe.name == 'Recipe x'


@pytest.mark.django_db
def test_recipe_details(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()
    response = client.get(f'/recipe/details/{recipe.id}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_delete(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()

    assert Recipe.objects.filter(id=recipe.id).exists()

    url = reverse('recipe-delete', args=[recipe.id])
    response = client.post(url)

    assert response.status_code == 302
    assert not Recipe.objects.filter(id=recipe.id).exists()


@pytest.mark.django_db
def test_recipe_update(client, user, set_up):
    client.login(username='Superadmin', password='123password')
    recipe = Recipe.objects.first()
    existing_ingredients = recipe.ingredients.all()

    assert existing_ingredients.count() > 0

    url = reverse('recipe-update', args=[recipe.id])

    data = {'name': 'Spaghetti',
            'description': 'xyz',
            'link': 'www.spaghetti.com',
            'portions': 10,
            'user': user.id}

    updated_ingredients_data = [
        {'id': ingredient.id, 'name': 'pepper', 'quantity': 500, 'unit': 'g', 'category': 'vegetables'}
        for ingredient in existing_ingredients
    ]

    data['ingredients-TOTAL_FORMS'] = len(updated_ingredients_data)
    data['ingredients-INITIAL_FORMS'] = len(updated_ingredients_data)

    for index, ingredient_data in enumerate(updated_ingredients_data):
        for key, value in ingredient_data.items():
            data[f'ingredients-{index}-{key}'] = value

    response = client.post(url, data)

    assert response.status_code == 302

    recipe.refresh_from_db()

    assert recipe.name == 'Spaghetti'
    assert recipe.portions == 10

    updated_ingredients = Ingredient.objects.filter(recipe=recipe)

    assert updated_ingredients[0].name == 'pepper'
    assert updated_ingredients[0].quantity == 500


