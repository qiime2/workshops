from django.utils.deprecation import MiddlewareMixin

from subdomains.middleware import SubdomainURLRoutingMiddleware


class PatchedSubdomainURLRoutingMiddleware(MiddlewareMixin,
                                           SubdomainURLRoutingMiddleware):
    pass
