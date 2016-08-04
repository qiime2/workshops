from django.http import HttpResponse
from django.shortcuts import render

TESTDATA = [{'text': 'Iceland!', 'workshop_slug': 'iceland-2016'}]


# Create your views here.
def index(request):
    return render(request,
                  'payments/index.html',
                  {'upcoming_workshops': TESTDATA})


def details(request, workshop_slug):
    return render(request,
                  'payments/detail.html')


def confirm(request, workshop_slug):
    return render(request,
                  'payments/confirm.html')
