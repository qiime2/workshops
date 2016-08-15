from django.conf import settings


def contact_info(request):
    return {'TECHNICAL_CONTACT': settings.TECHNICAL_CONTACT}
