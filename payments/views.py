from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import FormMixin
from django.conf import settings

import requests

from .models import Workshop, Order, OrderItem
from .forms import OrderForm


class WorkshopList(TemplateView):
    template_name = 'payments/workshop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_workshops'] = Workshop.objects \
            .filter(closing_date__gte=timezone.now())
        context['past_workshops'] = Workshop.objects \
            .filter(closing_date__lt=timezone.now())
        return context


class WorkshopDetail(FormMixin, DetailView):
    model = Workshop
    form_class = OrderForm
    context_object_name = 'workshop'

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
        order = form.data.copy()
        order['workshop'] = self.object.slug
        order_total = 0
        for rate in form.rate_set:
            order_total += Decimal(form.data[rate.name]) * rate.price

        order['order_total'] = str(order_total)
        self.request.session['order'] = order
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payments:confirm',
                       kwargs={'workshop_slug': self.object.slug})


class ConfirmOrder(TemplateView):
    template_name = 'payments/workshop_confirm.html'

    # TODO: refactor as a mixin and apply to confirm and the intermediate
    # view that does not yet exist
    def get(self, request, *args, **kwargs):
        if 'account' not in request.session:
            url = reverse('payments:details',
                          kwargs={'slug': kwargs['workshop_slug']})
            return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.session['order']
        order.pop('csrfmiddlewaretoken')
        context['order'] = order
        return context


class SubmitOrder(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_data = request.session['order']
        workshop = Workshop.objects.get(slug=order_data['workshop'])
        order = Order.objects.create(contact_email=order_data['email'],
                                     order_total=order_data['order_total'])
        for rate in workshop.rate_set.all():
            if order_data[rate.name] != 0:
                OrderItem.objects.create(order=order, rate=rate,
                                         # TODO: Fix this
                                         email=order_data['email'])

        # Now that the order is saved, clear the session so that they cant
        # resubmit the order
        request.session.flush()

        payload = {
            'LMID':         settings.LMID,
            'unique_id':    str(order.transaction_id),
            'sTotal':       str(order.order_total),
            'webTitle':     settings.PAYMENT_TITLE,
            'Trans_Desc':   settings.PAYMENT_DESCRIPTION,
            'contact_info': settings.PAYMENT_CONTACT_INFO
        }
        r = requests.post(settings.PAYMENT_URL, data=payload,
                          verify=settings.PAYMENT_CERT_BUNDLE)
        # TODO: We should use something like lxml2 to parse the form, then do
        # the second post on behalf of the customer, instead of just returning
        # the intermediate form as-is.
        return HttpResponse(r.text)
