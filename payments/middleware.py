# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib import messages


from subdomains.middleware import SubdomainURLRoutingMiddleware


class PatchedSubdomainURLRoutingMiddleware(MiddlewareMixin,
                                           SubdomainURLRoutingMiddleware):
    pass


if settings.DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    class PatchedDebugToolbarMiddleware(MiddlewareMixin,
                                        DebugToolbarMiddleware):
        pass


class CookieValidationMiddleware:
    request = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.request:
            if not request.COOKIES.get('valid_config') and request.path != '/':
                messages.warning(request, 'This site requires cookies. Please '
                                 'enable cookies and try again.')
                request.path_info = '/'

        response = self.get_response(request)
        response.set_cookie('valid_config', 'true')

        if not self.request:
            self.request = request

        return response
