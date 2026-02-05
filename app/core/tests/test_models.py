"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.cz', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful."""
        email = "test@example.cz"
        password = "pass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password)  # type: ignore

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normolized(self):
        """Test email normolized for new user."""

        email_samples = [
            ['test1@EXAMPLE.cz', 'test1@example.cz'],
            ['Test2@Example.cz', 'Test2@example.cz'],
            ['TEST3@EXAMPLE.CZ', 'TEST3@example.cz'],
            ['test4@example.CZ', 'test4@example.cz']
        ]

        for email, expected in email_samples:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test crating a superuser."""
        user = get_user_model().objects.create_superuser(
            email="admin@example.cz",
            password="adminpasswd123"
        )   # type: ignore

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_creat_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.cz',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_clear_tag(self):
        """Test create tag successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_creat_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Salt'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
