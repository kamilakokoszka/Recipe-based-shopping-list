from shopping_list_app.models import Recipe, Ingredient, IndependentIngredient, ShoppingList
import pytest


@pytest.mark.django_db
def test_recipe_list(client, set_up):
    response = client.get('/recipe/list/')

    assert response.status_code == 200
    assert Recipe.objects.count() == len(response.data)
