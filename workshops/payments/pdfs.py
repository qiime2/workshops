import os
from io import BytesIO

from xhtml2pdf import pisa

from django.conf import settings
from django.template.loader import render_to_string


def render_pdf(template_path: str, params: dict):
    params['MAILING_ADDRESS'] = settings.MAILING_ADDRESS
    params['BANK_INFO'] = settings.BANK_INFO
    html = render_to_string(template_path, params)
    response = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=fetch_resources)
    return response.getvalue()


def display_html(template_path: str, params: dict):
    params['MAILING_ADDRESS'] = settings.MAILING_ADDRESS
    params['BANK_INFO'] = settings.BANK_INFO
    return render_to_string(template_path, params)


# Taken from the xhtml2pdf docs
# https://xhtml2pdf.readthedocs.io/en/latest/usage.html#using-xhtml2pdf-in-django
def fetch_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path
