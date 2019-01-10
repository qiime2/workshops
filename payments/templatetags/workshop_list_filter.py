# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def workshop_history(workshops, category):
    result = workshops
    if category == 'upcoming':
        result = workshops.filter(
            start_date__gte=timezone.now()).order_by('start_date')
    elif category == 'past':
        result = workshops.filter(
            start_date__lt=timezone.now()).order_by('-start_date')
    return result
