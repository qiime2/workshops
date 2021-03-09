# ----------------------------------------------------------------------------
# Copyright (c) 2016-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from django.urls import path, include

from .views import (
    WorkshopList, SubmitOrder, WorkshopDetail, OrderDetail, ConfirmOrder, OrderCallback)

app_name = 'payments'
urlpatterns = [
    path('', WorkshopList.as_view(), name='index'),
    path('confirm/', OrderCallback.as_view(), name='callback'),
    path('submit/', SubmitOrder.as_view(), name='submit'),
    path('<slug:slug>/', include([
        path('', WorkshopDetail.as_view(), name='details'),
        path('order/', OrderDetail.as_view(), name='order_details'),
        path('confirm/', ConfirmOrder.as_view(), name='confirm'),
    ]))
]
