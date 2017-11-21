from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin,\
    LoginRequiredMixin
from complaint.models import Complaint
from CholitoProject.userManager import get_user_index
from municipality.fusioncharts import FusionCharts


class IndexView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_complaints_main.html'
    context = {}

    def getComplaintStats(self, complaints):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_STATUS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.status)
            stats_complaint[temp_status] += 1

        return stats_complaint

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(
            municipality=user.municipality)

        self.context['complaints'] = complaints
        self.context['c_user'] = user
        self.context['stats'] = self.getComplaintStats(complaints)
        return render(request, self.template_name, context=self.context)


class StatisticsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_statistics.html'
    context = {}

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user
        return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        if 'avatar' in request.FILES:
            c_user.municipality.avatar = request.FILES['avatar']
            c_user.municipality.save()
        return redirect('/')

def chart_cases(request):
    data = Complaint.len_case()
    # Create an object for the pie3d chart using the FusionCharts class constructor
    pie3d = FusionCharts("pie3d", "ex2", "100%", "400", "chart-1", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                         """{
                             "chart": {
                                 "caption": "Casos de Denuncia distribucion por tipos",
                                 "subcaption": "Municipalidad de Santiago",
                                 "startingangle": "120",
                                 "showlabels": "0",
                                 "showlegend": "1",
                                 "enablemultislicing": "0",
                                 "slicingdistance": "15",
                                 "showpercentvalues": "1",
                                 "showpercentintooltip": "0",
                                 "plottooltext": "Tipo de Denuncia : $label Total visit : $datavalue",
                                 "theme": "ocean"
                             },
                             "data": [
                                 {"label": "Abandonado en la calle", "value": """ + str(
                             data["Abandonado en la calle"]) + """},
                {"label": "Exposicion a temperaturas extremas", "value": """ + str(
                             data["Exposición a temperaturas extremas"]) + """},
                {"label": "Falta de Agua", "value": """ + str(data["Falta de agua"]) + """},
                {"label": "Falta de Comida", "value": """ + str(data["Falta de comida"]) + """},
                {"label": "Violencia", "value": """ + str(data["Violencia"]) + """},
                {"label": "Venta Ambulante", "value": """ + str(data["Venta Ambulante"]) + """}

            ]
    }""")
    return render(request, 'muni_statistics.html', {'output': pie3d.render()})


def chart_status(request):
    data = Complaint.status_last_week()
    # Create an object for the column2d chart using the FusionCharts class constructor
    column2d = FusionCharts("column2d", "ex1", "1000", "600", "chart-1", "json",
                            # The data is passed as a string in the `dataSource` as parameter.
                            """{  
                               "chart":{  
                                   "caption":"Frecuencia de denuncias por estado",
                                   "subCaption":"En los ultimos 7 dias",
                                   "theme":"ocean"
                               },
                               "data": [
                                   {"label": "Reportada", "value": """ + str(data["Reportada"]) + """},
                {"label": "Consolidada", "value": """ + str(
                                data["Consolidada"]) + """},
                {"label": "Verificada", "value": """ + str(data["Verificada"]) + """},
                {"label": "Cerrada", "value": """ + str(data["Cerrada"]) + """},
                {"label": "Desechada", "value": """ + str(data["Desechada"]) + """}

            ]
        }""")

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request, 'muni_statistics.html', {'output': column2d.render()})