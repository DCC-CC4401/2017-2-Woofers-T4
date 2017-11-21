from django.conf.urls import url

from ong.views import *
app_name = 'ong'

urlpatterns = [
    url(r'^ong/(?P<pk>\d+)/$', ONGNaturalView.as_view(), name='ong-logged'),
]