from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import requests
from .models import Address
from .serializers import AddressSerializer

# Create your views here.

def index(request):
    return render(request, 'addresses/index.html')

class AddressSearchView(APIView):
    def post(self, request):
        # Validation du payload
        query = request.data.get('q')
        if not query or not isinstance(query, str):
            return Response(
                {"error": "Le champ 'q' est requis et doit être une chaîne non vide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Appel à l'API Adresse (BAN)
            ban_response = requests.get(
                'https://api-adresse.data.gouv.fr/search/',
                params={'q': query, 'limit': 1}
            )
            ban_response.raise_for_status()
            data = ban_response.json()

            if not data.get('features'):
                return Response(
                    {"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extraction des données de l'adresse
            feature = data['features'][0]
            properties = feature['properties']
            geometry = feature['geometry']

            # Création de l'adresse en base
            address_data = {
                'label': properties['label'],
                'housenumber': properties['housenumber'],
                'street': properties['street'],
                'postcode': properties['postcode'],
                'citycode': properties['citycode'],
                'latitude': geometry['coordinates'][1],
                'longitude': geometry['coordinates'][0]
            }

            address = Address.objects.create(**address_data)
            serializer = AddressSerializer(address)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.RequestException:
            return Response(
                {"error": "Erreur serveur : impossible de contacter l'API externe."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AddressRisksView(APIView):
    def get(self, request, id):
        try:
            address = Address.objects.get(id=id)
            # Appel à l'API Géorisques
            georisques_response = requests.get(
                'https://georisques.gouv.fr/api/v1/resultats_rapport_risque',
                params={'latlon': f"{address.longitude},{address.latitude}"}
            )
            georisques_response.raise_for_status()
            return Response(georisques_response.json(), status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response(
                {"error": "Adresse non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
        except requests.RequestException:
            return Response(
                {"error": "Erreur serveur : échec de la récupération des données de Géorisques."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
