from django.db import models
from django.utils import timezone

from municipality.models import Municipality


class AnimalType(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    COMPLAINT_OPTIONS = (
        (1, "Abandono en la calle"),
        (2, "Exposición a temperaturas extremas"),
        (3, "Falta de agua"),
        (4, "Falta de comida"),
        (5, "Violencia"),
        (6, "Venta ambulante"),
    )

    COMPLAINT_STATUS = (
        (1, "Reportada"),
        (2, "Consolidada"),
        (3, "Verificada"),
        (4, "Cerrada"),
        (5, "Desechada"),
    )

    GENDER_OPTIONS = (
        (1, "Macho"),
        (2, "Hembra"),
        (3, "Desconocido")
    )

    WOUND_OPTIONS = (
        (1, "Sí"),
        (2, "No"),
        (3, "Desconocido")
    )

    description = models.TextField(max_length=1000, blank=True, null=True)
    case = models.SmallIntegerField(choices=COMPLAINT_OPTIONS, default=1)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    directions = models.TextField(max_length=200)
    status = models.SmallIntegerField(choices=COMPLAINT_STATUS, default=1)
    animal_type = models.ForeignKey(AnimalType)
    gender = models.SmallIntegerField(choices=GENDER_OPTIONS, default=3)
    wounded = models.SmallIntegerField(choices=WOUND_OPTIONS, default=3)
    color = models.TextField(max_length=50, blank=True, null=True)
    sent = models.DateTimeField(default=timezone.now)

    # TODO: required?
    municipality = models.ForeignKey(Municipality)

    def __str__(self):
        return "Complaint #" + str(self.pk)

    @staticmethod
    def len_case():
        cases = {
            "Abandonado en la calle":0,
            "Exposición a temperaturas extremas":0,
            "Falta de agua":0,
            "Falta de comida":0,
            "Violencia":0,
            "Venta Ambulante":0
        }
        queries = Complaint.objects.all().values()
        for index in range(0,len(queries)):
            if queries[index]['case'] == 1:
                cases["Abandonado en la calle"] += 1
            elif queries[index]['case'] == 2:
                cases["Exposición a temperaturas extremas"] += 1
            elif queries[index]['case'] == 3:
                cases["Falta de agua"] += 1
            elif queries[index]['case'] == 4:
                cases["Falta de comida"] += 1
            elif queries[index]['case'] == 5:
                cases["Violencia"] += 1
            elif queries[index]['case'] == 6:
                cases["Venta ambulante"] += 1
        return cases



class ComplaintImage(models.Model):
    image = models.ImageField(upload_to='complaints/', blank=True)
    complaint = models.ForeignKey('Complaint', on_delete=models.CASCADE)
