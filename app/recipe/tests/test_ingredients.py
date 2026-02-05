"""
Tests for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


def create_user(email='user@example.cz', password='pass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(
            email=email, password=password)   # type: ignore


def detail_url(ingredient_id):
    """Create and return ingredient detail url."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientAPITests(TestCase):
    """Tests unathenticated API requests."""

    def setUp(self):
        self.user = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Tests authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving ingredients list."""
        Ingredient.objects.create(user=self.user, name='Banana')
        Ingredient.objects.create(user=self.user, name='Kale')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)   # type: ignore

    def test_igredients_limited_to_user(self):
        """Test ingredients list is limited to authenticated user."""
        user2 = create_user(email='user2@example.cz')
        Ingredient.objects.create(user=user2, name='Vanila')
        ingredient = Ingredient.objects.create(user=self.user, name='Chili')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)   # type: ignore
        self.assertEqual(res.data[0]['name'], ingredient.name)   # type: ignore
        self.assertEqual(res.data[0]['id'], ingredient.id)   # type: ignore

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name="Peanut")

        paylaod = {'name': 'Kapusta'}
        url = detail_url(ingredient.id)   # type: ignore
        res = self.client.patch(url, paylaod)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, paylaod['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredients."""
        ingredient = Ingredient.objects.create(user=self.user, name='Tomato')

        url = detail_url(ingredient.id)   # type: ignore
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
