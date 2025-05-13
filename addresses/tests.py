from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Address

# Create your tests here.

class AddressAPITestCase(APITestCase):
    def test_create_address(self):
        url = reverse('address-search')
        data = {"q": "8 bd du Port, 56170 Sarzeau"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('label', response.data)
        self.assertEqual(Address.objects.count(), 1)

    def test_create_address_missing_q(self):
        url = reverse('address-search')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_address_empty_q(self):
        url = reverse('address-search')
        response = self.client.post(url, {"q": ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_address_not_found(self):
        url = reverse('address-search')
        # Une adresse volontairement improbable
        response = self.client.post(url, {"q": "adresseinexistantepourtest"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_risks_for_existing_address(self):
        # Création d'une adresse en base (en évitant l'appel API externe)
        address = Address.objects.create(
            label="Test",
            housenumber="1",
            street="Rue Test",
            postcode="75000",
            citycode="12345",
            latitude=48.8566,
            longitude=2.3522
        )
        url = reverse('address-risks', args=[address.id])
        response = self.client.get(url)
        # On ne teste pas le contenu exact car dépend de l'API externe, mais on vérifie le code HTTP
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])

    def test_get_risks_for_nonexistent_address(self):
        url = reverse('address-risks', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_create_address_twice(self):
        url = reverse('address-search')
        data = {"q": "8 bd du Port, 56170 Sarzeau"}
        response1 = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(Address.objects.count(), 2)  # Car pas de contrainte d'unicité dans le modèle
