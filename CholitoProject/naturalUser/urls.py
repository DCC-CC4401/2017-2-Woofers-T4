from django.conf.urls import include, url

from .views import *

from django.conf import settings

urlpatterns = [
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^type-user/$', ChooseUserReg.as_view(), name='choose-register'),
    url(r'^$', IndexView.as_view(), name='user-index'),
    # for now
    url(r'^user/$', UserDetail.as_view(), name='user-update'),
    url(r'^user-ong-in/$', OngInViewTemplate.as_view(), name='user-ong-in'),
    url(r'^user-ong-out/$', OngOutViewTemplate.as_view(), name='user-ong-out'),
    url(r'^show/ong/$', ONGListView.as_view(), name='show-ong'),
    url(r'^show/animals/$', AnimalListView.as_view(), name='show-animals'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
