from django.conf.urls import url

from . import views

app_name = 'payments'
urlpatterns = [
    url(r'^$', views.index,
        name='index'),
    url(r'^(?P<workshop_slug>[\w\-]+)/$', views.details,
        name='details'),
    url(r'^(?P<workshop_slug>[\w\-]+)/confirm/$', views.confirm,
        name='confirm')
]
