from django.utils.deprecation import MiddlewareMixin

from subdomains.middleware import SubdomainURLRoutingMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware


class PatchedSubdomainURLRoutingMiddleware(MiddlewareMixin,
                                           SubdomainURLRoutingMiddleware):
    pass


class PatchedDebugToolbarMiddleware(MiddlewareMixin, DebugToolbarMiddleware):
    pass
