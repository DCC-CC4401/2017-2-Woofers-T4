from django.contrib.auth.models import User, Permission
from django.db import models
from django.shortcuts import render

from ong.models import ONG

class NaturalUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='n_users/avatar/')

    def save(self, *args, **kwargs):
        super(NaturalUser, self).save(*args, **kwargs)
        if not self.user.has_perm('natural_user_access'):
            permission = Permission.objects.get(codename='natural_user_access')
            self.user.user_permissions.add(permission)
        self.user.save()

    def __str__(self):
        return "Natural user " + self.user.username

    def get_index(self, request, context=None):
        liked = ONG.objects.filter(onglike__natural_user=self)
        not_liked = ONG.objects.exclude(pk__in=liked.values_list('pk', flat=True))
        context['liked_ongs'] = liked
        context['ongs'] = not_liked
        print([ong.name for ong in liked])
        print([ong.name for ong in not_liked])
        return render(request, 'index.html', context=context)


class Favorites(models.Model):
    natural_user = models.ForeignKey(NaturalUser)
    ong = models.ForeignKey(ONG)

    def __str__(self):
        return self.idPersona
