from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect


class Municipality(models.Model):
    name = models.TextField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    directions = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.name


# TODO: Add profile image field
class MunicipalityUser(models.Model):
    user = models.OneToOneField(User)
    municipality = models.ForeignKey('Municipality')

    def __str__(self):
        return self.municipality.name + " User"

    def get_index(self):
        return redirect('municipality-index', pk=self.pk)
