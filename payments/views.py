from django.core.urlresolvers import reverse
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


class WorkshopDetail(FormMixin, DetailView):
    model = Workshop
    form_class = OrderForm
    context_object_name = 'workshop'
    template_name = 'payments/detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['workshop'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        rates = []
        for rate in self.object.rate_set.order_by('price'):
            field = context['form'][rate.name]
            rates.append({'field': field, 'name': rate.name, 'price':
                          rate.price})
        context['rates'] = rates
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        self.request.session['order'] = form.data
        return form_valid

    def get_success_url(self):
        return reverse('payments:confirm',
                       kwargs={'workshop_slug': self.object.slug})


def confirm(request, workshop_slug):
    order = request.session['order']
    order.pop('csrfmiddlewaretoken')
    return render(request,
                  'payments/confirm.html',
                  context={'order': order})
