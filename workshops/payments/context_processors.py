# ----------------------------------------------------------------------------
# Copyright (c) 2016-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.conf import settings


def contact_info(request):
    return {
        'REQUEST_CONTACT': settings.REQUEST_CONTACT,
        'TECHNICAL_CONTACT': settings.TECHNICAL_CONTACT,
    }
