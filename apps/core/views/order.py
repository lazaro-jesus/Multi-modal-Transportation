from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from ..models import Order
from ..forms import OrderForm


class OrderCreateView(CreateView):
    template_name = 'generic/create.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('core:order-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name
        return context
    

class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name_plural
        return context