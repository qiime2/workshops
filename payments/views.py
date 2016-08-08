from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import FormMixin
from django.conf import settings

import requests
from extra_views import FormSetView

from .models import Workshop, Order, OrderItem, Rate
from .forms import OrderForm, OrderDetailForm


class SessionConfirmMixin(object):
    def get(self, request, *args, **kwargs):
        if 'order' not in request.session:
            url = reverse('payments:details',
                          kwargs={'slug': kwargs['slug']})
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)


class WorkshopList(TemplateView):
    template_name = 'payments/workshop_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_workshops'] = Workshop.objects \
            .filter(start_date__gte=timezone.now())
        context['past_workshops'] = Workshop.objects \
            .filter(start_date__lt=timezone.now())
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
        order['rates'] = list(form.rate_set.values('id', 'name'))
        order_total = 0
        for rate in form.rate_set:
            order_total += Decimal(form.data[rate.name]) * rate.price

        order['order_total'] = str(order_total)
        self.request.session['order'] = order
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payments:order_details',
                       kwargs={'slug': self.object.slug})


class OrderDetail(SessionConfirmMixin, FormSetView):
    template_name = 'payments/order_detail.html'
    form_class = OrderDetailForm
    extra = 0

    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs['slug']
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        order = self.request.session['order']
        initial = []
        for rate in order['rates']:
            for ticket in range(int(order[rate['name']])):
                data = {'rate': rate['id']}
                initial.append(data)
        self.initial = initial
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zipped = []
        for i, form in enumerate(context['formset']):
            rate = Rate.objects.get(pk=self.initial[i]['rate'])
            data = {'form': form, 'rate': rate}
            zipped.append(data)
        context['zipped'] = zipped
        context['workshop'] = Workshop.objects.get(slug=self.slug)
        return context

    def formset_valid(self, formset):
        suborder = formset.data.copy()
        order = self.request.session['order']
        tickets = []
        total_forms = suborder['form-TOTAL_FORMS']
        for i in range(int(total_forms)):
            rate = suborder['form-%s-rate' % i]
            email = suborder['form-%s-email' % i]
            name = suborder['form-%s-name' % i]
            tickets.append({'rate': rate, 'email': email, 'name': name})
        order['tickets'] = tickets
        self.request.session['order'] = order
        return super().formset_valid(formset)

    def get_success_url(self):
        return reverse('payments:confirm',
                       kwargs={'slug': self.slug})


class ConfirmOrder(SessionConfirmMixin, TemplateView):
    template_name = 'payments/workshop_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.session['order']
        tickets = []
        for ticket in order['tickets']:
            tickets.append({'name': ticket['name'], 'email': ticket['email'],
                            'rate': Rate.objects.get(pk=ticket['rate'])})
        context['tickets'] = tickets
        context['order_email'] = order['email']
        context['order_total'] = order['order_total']
        context['workshop'] = Workshop.objects.get(slug=kwargs['slug'])
        return context


class SubmitOrder(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_data = request.session['order']
        order = Order.objects.create(contact_email=order_data['email'],
                                     order_total=order_data['order_total'])
        for ticket in request.session['order']['tickets']:
            OrderItem.objects.create(order=order,
                                     rate_id=ticket['rate'],
                                     email=ticket['email'],
                                     name=ticket['name'])

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
