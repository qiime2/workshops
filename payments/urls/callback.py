# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^$', views.OrderCallback.as_view()),
]
