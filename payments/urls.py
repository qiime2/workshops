from django.conf.urls import url

from . import views

app_name = 'payments'
urlpatterns = [
    url(r'^$', views.WorkshopList.as_view(),
        name='index'),
    url(r'^(?P<slug>[\w\-]+)/$', views.WorkshopDetail.as_view(),
        name='details'),
    url(r'^(?P<workshop_slug>[\w\-]+)/confirm/$', views.confirm,
        name='confirm'),
    url(r'^(?P<workshop_slug>[\w\-]+)/submit/$', views.submit,
        name='submit')
]
