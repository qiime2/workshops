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
