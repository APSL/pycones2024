# Create your tests here.

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@pytest.mark.django_db
class AdminPackageTests(APITestCase):
    fixtures = ["initial_data", "test_data"]

    def setUp(self):
        self.client.force_authenticate(user=User.objects.get(username="PostalClerkTest"))

    def test_packages_list(self):
        assert False

    def test_packages_create(self):
        """
        Test creating a package using the admin API endpoint.
        """
        data = {
            "origin_address": dict(
                street_address="1234 Main Street",
                city="Anytown",
                state="NY",
                postal_code="12345",
                country="US",
            ),
            "destination_address": dict(
                street_address="1234 Second Street",
                city="Anytown",
                state="NY",
                postal_code="54321",
                country="US",
            ),
        }

        response = self.client.post(
            path=reverse("api:admin-packages"),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tracking_number", response.json())

    def test_packages_delete(self):
        url = reverse("api:admin-packages-archive", kwargs={"tracking_number": "987654321"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_packages_archive(self):
        pass


@pytest.mark.django_db
class CourierPackageTests(APITestCase):
    fixtures = ["initial_data", "test_data"]

    def setUp(self):
        self.client.force_authenticate(user=User.objects.get(username="CourierTest"))

    def test_packages_tracking_create(self):
        assert False


@pytest.mark.django_db
class AnonPackageTests(APITestCase):
    fixtures = ["initial_data", "test_data"]

    def test_packages_retrieve(self):
        assert False