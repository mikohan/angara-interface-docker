from rest_framework import APITestCase
from django.urls import reverse
from rest_framework import status


class HelloWorldTestCase(APITestCase):
    """First test case"""

    def test_hello_world(self):
        response = self.client.get(reverse("get-products-for-angara-procenka"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
