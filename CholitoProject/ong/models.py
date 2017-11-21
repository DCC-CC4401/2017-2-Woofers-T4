# Create your models here.

from django.contrib.auth.models import User, Permission
from django.db import models
from django.shortcuts import redirect


# Create your models here.


class ONG(models.Model):
    name = models.TextField(max_length=200, primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    directions = models.TextField(max_length=200, null=True)
    avatar = models.ImageField(upload_to='ong/avatar/')

    def __str__(self):
        return self.name + " ONG"


class ONGUser(User):
    ong = models.ForeignKey('ONG')
    user = models.OneToOneField(User)

    def __str__(self):
        return self.ong.name

    def get_index(self, request, context):
        return redirect('/ong/')

    def save(self, *args, **kwargs):
        super(ONGUser, self).save(*args, **kwargs)
        if not self.user.has_perm('ong_user_access'):
            permission = Permission.objects.get(
                codename='ong_user_access')
            self.user.user_permissions.add(permission)
        self.user.save()
