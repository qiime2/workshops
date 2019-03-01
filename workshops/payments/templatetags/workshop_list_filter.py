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
