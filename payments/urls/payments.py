# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.conf.urls import url

from ..import views

app_name = 'payments'
urlpatterns = [
    url(r'^$', views.WorkshopList.as_view(),
        name='index'),
    url(r'^submit/$', views.SubmitOrder.as_view(),
        name='submit'),
    url(r'^(?P<slug>[\w\-]+)/$', views.WorkshopDetail.as_view(),
        name='details'),
    url(r'^(?P<slug>[\w\-]+)/order/$', views.OrderDetail.as_view(),
        name='order_details'),
    url(r'^(?P<slug>[\w\-]+)/confirm/$', views.ConfirmOrder.as_view(),
        name='confirm')
]
