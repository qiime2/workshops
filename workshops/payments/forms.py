# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import functools

from django import forms

from .models import PosterOption, MeetingOption


class OrderForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Orderer's Name",
                                      'class': 'input'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': "Orderer's Email Address",
                                      'class': 'input'})
    )

    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        discount_code = kwargs.pop('discount_code')
        super().__init__(*args, **kwargs)

        self.rate_set = workshop.filter_rates(discount_code)
        for rate in self.rate_set:
            self.fields[rate.name] = forms.IntegerField(
                initial=0,
                min_value=0,
                max_value=rate.max_order if rate.max_order else rate.capacity - rate.ticket_count,
                widget=forms.NumberInput(attrs={'class': 'input'})
            )
        for rate in workshop.sold_out_rates.all():
            self.fields[rate.name] = forms.IntegerField(
                initial=0,
                min_value=0,
                disabled=True,
                widget=forms.NumberInput(attrs={'class': 'input'})
            )

    def clean(self):
        cleaned_data = super().clean()
        rates = {}
        for rate in self.rate_set:
            try:
                rates[rate.name] = cleaned_data[rate.name]
            except KeyError:
                return cleaned_data

        if not functools.reduce(lambda x, y: x + y, rates.values()):
            raise forms.ValidationError('Order can not be empty.')

        return cleaned_data


class OrderDetailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        super().__init__(*args, **kwargs)
        poster_qs = PosterOption.objects.filter(workshop__slug=workshop)
        if poster_qs.count() != 0:
            self.fields['poster_option'] = forms.ModelChoiceField(
                queryset=poster_qs)

        meeting_qs = MeetingOption.objects.filter(workshop__slug=workshop)
        if meeting_qs.count() != 0:
            self.fields['meeting_option'] = forms.ModelChoiceField(
                queryset=meeting_qs)

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Email',
                                      'class': 'input'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Name',
                                      'class': 'input'})
    )
    rate = forms.CharField(widget=forms.HiddenInput())


class OrderDetailFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        emails = []
        for form in self.forms:
            email = form.cleaned_data['email']
            if email in emails:
                raise forms.ValidationError('Tickets must have a unique '
                                            'email address.')
            emails.append(email)
