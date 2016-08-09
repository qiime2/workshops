from django.conf import settings
from django.conf.urls import include, url
from django.views import defaults as default_views


urlpatterns = [
    url(r'^', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]
