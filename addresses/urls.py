from django.urls import path
from .views import AddressSearchView, AddressRisksView, index

urlpatterns = [
    path('', index, name='index'),
    path('addresses/', AddressSearchView.as_view(), name='address-search'),
    path('addresses/<int:id>/risks/', AddressRisksView.as_view(), name='address-risks'),
] 