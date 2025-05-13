from django.db import models

# Create your models here.

class Address(models.Model):
    label = models.CharField(max_length=255)
    housenumber = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    citycode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
