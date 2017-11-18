from django.conf.urls import url
from ong.views import SignUpView

urlpatterns = [
	url(r'^register-ong/$', SignUpView.as_view(), name='register-ong'),
]

