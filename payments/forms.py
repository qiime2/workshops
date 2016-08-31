# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import functools

from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Orderer's Name",
                                      'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': "Orderer's Email Address",
                                      'class': 'form-control'})
    )
    special_code = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Discount Code',
                                      'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        super().__init__(*args, **kwargs)

        self.rate_set = workshop.available_rates.order_by('price')
        for rate in self.rate_set:
            self.fields[rate.name] = forms.IntegerField(
                initial=0,
                min_value=0,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
        for rate in workshop.sold_out_rates.all():
            self.fields[rate.name] = forms.IntegerField(
                initial=0,
                min_value=0,
                disabled=True,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
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
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Email',
                                      'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ticketholder\'s Name',
                                      'class': 'form-control'})
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
