# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from subdomains.middleware import SubdomainURLRoutingMiddleware


class PatchedSubdomainURLRoutingMiddleware(MiddlewareMixin,
                                           SubdomainURLRoutingMiddleware):
    pass


if settings.DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    class PatchedDebugToolbarMiddleware(MiddlewareMixin,
                                        DebugToolbarMiddleware):
        pass
