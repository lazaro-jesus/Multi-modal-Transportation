import pandas as pd

from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from .cvxpy import CVXPY
from .route import Route
from .location import Location
from .error import NotSolvable
from .validations import validate_max_value, validate_letters


class Order(models.Model):
    ship_from = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de origen", related_name="orders_from")
    ship_to = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de destino", related_name="orders_to")
    commodity = models.CharField(max_length=255, verbose_name="Mercancía", validators=[validate_letters])
    value = models.IntegerField(verbose_name="Valor de la mercancía")
    volume = models.IntegerField(verbose_name="Volumen", default=0, validators=[validate_max_value])
    date = models.DateField(verbose_name="Fecha", auto_now_add=True)
    required_delivery_date = models.DateField(verbose_name="Fecha de entrega requerida")
    tax_percentage = models.FloatField(verbose_name="Porcentaje de impuesto", default=0)
    
    class Meta:
        verbose_name = "Órden"
        verbose_name_plural = "Órdenes"

    def __str__(self) -> str:
        return f"{self.commodity} - {self.ship_from} to {self.ship_to}"

    @cached_property
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "Order Number": [self.pk],
            "Ship From": [self.ship_from.to_calculate],
            "Ship To": [self.ship_to.to_calculate],
            "Commodity": [self.commodity],
            "Order Value": [self.value],
            "Volume": [self.volume],
            "Order Date": [pd.to_datetime(self.date, format="%d/%m/%Y")],
            "Required Delivery Date": [pd.to_datetime(self.required_delivery_date, format="%d/%m/%Y")],
            "Tax Percentage": [self.tax_percentage]
        })
        
    def update_optimize_route(self, optimized, routes, solved):
       optimized.routes = routes
       optimized.solved = solved
       optimized.save()
    
    def optimize_route(self) -> None:
       order = self.to_dataframe
       routes = Route.objects.routes_dataframe()
       m = CVXPY()
       
       try:
          m.set_param(routes, order)
          m.build_model()
          m.solve_model()
       except Exception:
          optimized = OrderOptimized.objects.filter(order__pk=self.pk).first()

          if optimized is not None:
             self.update_optimize_route(
                 optimized,
                 "El modelo no tiene solución. Revise el tiempo de tránsito, rutas y fecha de entrega.",
                 False
             )
          else:
             OrderOptimized.objects.create(
                 order=self,
                 routes="El modelo no tiene solución. Revise el tiempo de tránsito, rutas y fecha de entrega.",
                 solved=False
             )
       try:
          solution = m.solution_text(order)
          optimized = OrderOptimized.objects.filter(order__pk=self.pk).first()

          if optimized is not None:
             self.update_optimize_route(optimized, solution, True)
          else:
             OrderOptimized.objects.create(order=self, routes=solution)
       except NotSolvable as error:
           optimized = OrderOptimized.objects.filter(order__pk=self.pk).first()

           if optimized is not None:
               optimized.routes = error.args[0]
               optimized.solved = False
               optimized.save()
           else:
               OrderOptimized.objects.create(order=self, routes=error.args[0], solved=False)

        
class OrderOptimized(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Órden", related_name="optimized")
    routes = models.TextField(verbose_name="Rutas Optimizadas")
    solved = models.BooleanField(default=True, verbose_name="Solucionado")

    def __str__(self) -> str:
        return f"{self.order.commodity} - {self.order.ship_from} to {self.order.ship_to}"
    
    def to_list(self):
        icons = {
            "AI": "bi bi-airplane-fill text-info",
            "RA": "bi bi-train-front-fill text-danger",
            "TR": "bi bi-truck text-warning",
            "SE": "bi bi-water text-primary"
        }
        solutions = self.routes.split(";")
        locations = Location.objects.all()
        routes = []

        for i in range(0, len(solutions), 4):
            source = [location for location in locations if location.to_calculate == solutions[i+2]][0]
            destination = [location for location in locations if location.to_calculate == solutions[i+3]][0]
            route = Route.objects.filter(Q(source__pk=source.pk) & Q(destination__pk=destination.pk)).first()
            
            routes.append(
                {
                    "id": solutions[i],
                    "date": solutions[i+1],
                    "origin": solutions[i+2],
                    "destination": solutions[i+3],
                    "icon": icons[route.travel_mode]
                }
            )

        return routes