from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from CholitoProject.userManager import get_user_index
from complaint.forms import ComplaintForm, ImageForm
from complaint.models import Complaint, ComplaintImage, AnimalType

from complaint.fusioncharts import FusionCharts



class ComplaintView(View):
    form = ComplaintForm(
        initial={'directions': "beauchef"}, prefix='complaint')
    image_form = ImageForm(prefix='image')
    animals = AnimalType.objects.all()
    context = {'form': form, 'image_form': image_form, 'animals': animals}
    template_name = 'complaint.html'

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user
        return render(request, self.template_name, context=self.context)


class ComplaintSendView(View):
    def post(self, request, **kwargs):
        form = ComplaintForm(request.POST, prefix='complaint')
        image_form = ImageForm(request.POST, request.FILES, prefix='image')
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.status = 1
            complaint.save()
            if image_form.is_valid():
                image_ = image_form.cleaned_data.get('complaint_image')
                if image_ is not None:
                    ComplaintImage.objects.create(
                        complaint=complaint, image=image_)

        return redirect('/')


class ComplaintRenderView(PermissionRequiredMixin, LoginRequiredMixin, View):
    template_name = 'view_complaint.html'
    permission_required = 'municipality.municipality_user_access'
    context = {}

    def get(self, request, pk, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user
        complaint = get_object_or_404(Complaint, pk=pk)
        self.context['complaint'] = complaint

        images = ComplaintImage.objects.filter(complaint=complaint)
        self.context['images'] = images

        return render(request, self.template_name, context=self.context)


class ComplaintActState(PermissionRequiredMixin, LoginRequiredMixin, View):
    template_name = 'view_complaint.html'
    permission_required = 'municipality.municipality_user_access'
    context = {}

    def post(self, request, pk, **kwargs):
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = request.POST['status']
        complaint.save()

        self.context['complaint'] = complaint

        images = ComplaintImage.objects.filter(complaint=complaint)
        self.context['images'] = images
        # render(request, self.template_name, context=self.context)
        return redirect('see-complaint', pk=pk)

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
                {"label": "Abandonado en la calle", "value": """+str(data["Abandonado en la calle"])+"""},
                {"label": "Exposicion a temperaturas extremas", "value": """+str(data["Exposición a temperaturas extremas"])+"""},
                {"label": "Falta de Agua", "value": """+str(data["Falta de agua"])+"""},
                {"label": "Falta de Comida", "value": """+str(data["Falta de comida"])+"""},
                {"label": "Violencia", "value": """+str(data["Violencia"])+"""},
                {"label": "Venta Ambulante", "value": """+str(data["Venta Ambulante"])+"""}
                
            ]
    }""")
    return render(request, 'example.html', {'output': pie3d.render()})

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
    return render(request, 'example.html', {'output': column2d.render()})

