import os
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


def render(path: str, params: dict):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=fetch_resources)
    return response.getvalue()


# This was taken from the xhtml2pdf documentation then modified because they
# didn't account for ../ in relative filepaths and sRoot wasn't correct
def fetch_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    uri = uri.replace('../', '')
    # use short variable names
    sUrl = 'static/'
    sRoot = '../workshops/workshops/'

    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri)
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # This has no real effect, exceptions just cause the pdf to not have the image
    if not os.path.isfile(path):
        raise Exception(
            f'{path} is not a valid uri'
        )
    return path
