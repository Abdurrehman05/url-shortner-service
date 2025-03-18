from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from .models import URL

class URLModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.valid_url = URL.objects.create(
            long_url='https://www.example.com',
            short_url='abc123'
        )

    def test_url_creation(self):
        """Test that a URL can be created with valid data"""
        self.assertEqual(self.valid_url.long_url, 'https://www.example.com')
        self.assertEqual(self.valid_url.short_url, 'abc123')
        self.assertEqual(self.valid_url.access_count, 0)
        self.assertTrue(self.valid_url.is_active)

    def test_string_representation(self):
        """Test the string representation of URL model"""
        expected_string = f'{self.valid_url.short_url} -> {self.valid_url.long_url}'
        self.assertEqual(str(self.valid_url), expected_string)

    def test_invalid_url_format(self):
        """Test that invalid URL format raises ValidationError"""
        invalid_url = URL(long_url='not-a-valid-url', short_url='def456')
        with self.assertRaises(ValidationError):
            invalid_url.full_clean()

    def test_duplicate_short_url(self):
        """Test that duplicate short_url raises IntegrityError"""
        with self.assertRaises(IntegrityError):
            URL.objects.create(
                long_url='https://www.another-example.com',
                short_url='abc123'  # Same as self.valid_url
            )

    def test_access_count_increment(self):
        """Test access_count increment functionality"""
        initial_count = self.valid_url.access_count
        self.valid_url.increment_access_count()
        self.assertEqual(self.valid_url.access_count, initial_count + 1)

        # Refresh from database to verify persistence
        self.valid_url.refresh_from_db()
        self.assertEqual(self.valid_url.access_count, initial_count + 1)

    def test_url_deactivation(self):
        """Test URL deactivation"""
        self.valid_url.is_active = False
        self.valid_url.save()
        
        # Refresh from database to verify persistence
        self.valid_url.refresh_from_db()
        self.assertFalse(self.valid_url.is_active)

    def test_max_length_constraints(self):
        """Test URL length constraints"""
        # Test long_url max length (2048 characters)
        long_url = 'https://example.com/' + 'a' * 2048
        with self.assertRaises(ValidationError):
            url = URL(long_url=long_url, short_url='xyz789')
            url.full_clean()

class URLAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.valid_url = URL.objects.create(
            long_url='https://www.example.com',
            short_url='abc123'
        )
        self.api_url = '/api/urls/'

    def test_create_url(self):
        """Test creating a new URL through API"""
        data = {'long_url': 'https://www.test.com'}
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_url', response.data)
        self.assertEqual(response.data['long_url'], 'https://www.test.com')
        self.assertTrue(response.data['is_active'])

    def test_create_invalid_url(self):
        """Test creating a URL with invalid data"""
        data = {'long_url': 'not-a-valid-url'}
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_url(self):
        """Test retrieving a URL's details"""
        response = self.client.get(f'{self.api_url}{self.valid_url.short_url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['long_url'], 'https://www.example.com')
        self.assertEqual(response.data['access_count'], 1)  # Count increments on retrieve

    def test_retrieve_nonexistent_url(self):
        """Test retrieving a non-existent URL"""
        response = self.client.get(f'{self.api_url}nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_url(self):
        """Test deactivating a URL"""
        response = self.client.post(f'{self.api_url}{self.valid_url.short_url}/deactivate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify URL is deactivated
        self.valid_url.refresh_from_db()
        self.assertFalse(self.valid_url.is_active)

        # Test short_url max length (10 characters)
        with self.assertRaises(ValidationError):
            url = URL(long_url='https://example.com', short_url='a' * 11)
            url.full_clean()

class URLAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.valid_url = URL.objects.create(
            long_url='https://www.example.com',
            short_url='abc123'
        )
        self.api_url = '/api/urls/'

    def test_create_url(self):
        """Test creating a new URL through API"""
        data = {'long_url': 'https://www.test.com'}
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_url', response.data)
        self.assertEqual(response.data['long_url'], 'https://www.test.com')
        self.assertTrue(response.data['is_active'])

    def test_create_invalid_url(self):
        """Test creating a URL with invalid data"""
        data = {'long_url': 'not-a-valid-url'}
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_url(self):
        """Test retrieving a URL's details"""
        response = self.client.get(f'{self.api_url}{self.valid_url.short_url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['long_url'], 'https://www.example.com')
        self.assertEqual(response.data['access_count'], 1)  # Count increments on retrieve

    def test_retrieve_nonexistent_url(self):
        """Test retrieving a non-existent URL"""
        response = self.client.get(f'{self.api_url}nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_url(self):
        """Test deactivating a URL"""
        response = self.client.post(f'{self.api_url}{self.valid_url.short_url}/deactivate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify URL is deactivated
        self.valid_url.refresh_from_db()
        self.assertFalse(self.valid_url.is_active)
