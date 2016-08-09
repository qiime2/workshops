import functools

from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Order Email Address',
                                      'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        workshop = kwargs.pop('workshop')
        super().__init__(*args, **kwargs)

        self.rate_set = workshop.rate_set.order_by('price')
        for rate in self.rate_set:
            self.fields[rate.name] = forms.IntegerField(
                initial=0,
                min_value=0,
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
