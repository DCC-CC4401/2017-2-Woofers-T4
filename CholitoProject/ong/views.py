from django.views import View
from django.shortcuts import get_object_or_404

from CholitoProject.userManager import *
from django.shortcuts import render
from animals.models import Animal
from ong.models import ONG
from django.utils.deconstruct import deconstructible

# Create your views here.
class ONGNaturalView(View):
    animals = Animal.Objects.all()
    context = {'animales': animals}

    def get(self, request, id, **kwargs):
        user_actual = get_user_index(request.user)
        ong = get_object_or_404(ONG, pk=id)
        self.context['ong'] = ong
        self.context['usuario'] = user_actual
        self.context['animales'] = Animal.objects.filter(ong=ong)
        return render(request, 'ong-adopcion-en.html', context=self.context)
