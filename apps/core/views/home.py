from django.views.generic import TemplateView

from ..models import Route, Order, OrderOptimized, Province


class HomeView(TemplateView):
    template_name = "home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes_count'] = Route.objects.count()
        context['orders_count'] = Order.objects.count()
        context['processed_orders_count'] = OrderOptimized.objects.count()
        context['soved_orders_count'] = OrderOptimized.objects.filter(solved=True).count()
        context['provinces'] = Province.labels
        
        return context
