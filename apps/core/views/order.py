from django.views.generic import CreateView, ListView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
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
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        
        for key in form.errors.keys():
            form.fields[key].widget.attrs["class"] += " is-invalid"
            
        return response
    

class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name_plural
        return context
    

class OrderUpdateView(UpdateView):
    template_name = 'generic/update.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('core:order-list')
    
    def get_object(self, queryset=None):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name
        return context
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        
        for key in form.errors.keys():
            form.fields[key].widget.attrs["class"] += " is-invalid"
            
        return response

  
class OrderDeleteView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        order.delete()
        return redirect(reverse_lazy('core:order-list'))
    
class OrderOptimizeView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        order.optimize_route()
        return redirect('core:order-list')