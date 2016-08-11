from django import template


register = template.Library()


@register.inclusion_tag('payments/_form_errors.html')
def form_errors(form):
    return {'form': form}
