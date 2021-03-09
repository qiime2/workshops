# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django import template


register = template.Library()


@register.inclusion_tag('payments/_form_errors.html')
def form_errors(form):
    return {'form': form}
