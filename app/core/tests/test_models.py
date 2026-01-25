"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


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
