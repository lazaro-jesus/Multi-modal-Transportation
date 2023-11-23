from django import forms
from .models import Order, Route


# Formulario para Órdenes
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('ship_from', 'ship_to', 'commodity', 'value', 'volume', 'required_delivery_date', 'tax_percentage')
        widgets = {
            'ship_from': forms.Select(attrs={'class': 'form-select'}),
            'ship_to': forms.Select(attrs={'class': 'form-select'}),
            'commodity': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'required_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ship_from'].empty_label = "Seleccione el origen"
        self.fields['ship_to'].empty_label = "Seleccione el destino"


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = (
            'source',
            'destination',
            'container_size',
            'carrier',
            'travel_mode',
            'extra_cost',
            'custom_clearance_time',
            'handling_time',
            'extra_time',
            'transit_time'
        )
        widgets = {
            'source': forms.Select(attrs={'class': 'form-select'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'container_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'carrier': forms.TextInput(attrs={'class': 'form-control'}),
            'travel_mode': forms.Select(attrs={'class': 'form-select'}),
            'extra_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'custom_clearance_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'handling_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'transit_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].empty_label = "Seleccione el origen"
        self.fields['destination'].empty_label = "Seleccione el destino"