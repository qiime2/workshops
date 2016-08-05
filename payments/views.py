from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .models import Workshop
from .forms import OrderForm


class WorkshopList(ListView):
    queryset = Workshop.objects.filter(start_date__gte=timezone.now())
    template_name = 'payments/index.html'
    context_object_name = 'upcoming_workshops'


class WorkshopDetail(DetailView):
    model = Workshop
    context_object_name = 'workshop'
    template_name = 'payments/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = self.object.rate_set.order_by('price')
        context['order_form'] = OrderForm(workshop=self.object)
        return context


def confirm(request, workshop_slug):
    return render(request,
                  'payments/confirm.html')
