import pandas as pd

from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError

from .cvxpy import CVXPY
from .constants import Status
from .location import Location
from .route import Route
from .error import NotSolvable


def validate_max_value(value) -> None:
   if value > 100:
       raise ValidationError(
           "%(value)s es mayor que el valor máximo permitido (100)",
           params={"value": value},
       )


class Order(models.Model):
    ship_from = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de origen", related_name="orders_from")
    ship_to = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de destino", related_name="orders_to")
    commodity = models.CharField(max_length=255, verbose_name="Mercancía")
    value = models.IntegerField(verbose_name="Valor")
    volume = models.IntegerField(verbose_name="Volumen", default=0, validators=[validate_max_value])
    date = models.DateField(verbose_name="Fecha", auto_now_add=True)
    required_delivery_date = models.DateField(verbose_name="Fecha de entrega requerida")
    tax_percentage = models.FloatField(verbose_name="Porcentaje de impuesto", default=0)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ON_HOLD, verbose_name="Estado")
    
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
    
    def optimize_route(self) -> str:
        order = self.to_dataframe
        routes = Route.objects.routes_dataframe()
        m = CVXPY()
        m.set_param(routes, order)
        m.build_model()
        m.solve_model()
        
        try:
            solution = m.solution_text(order)
            optimized, _ = OrderOptimized.objects.get_or_create(order=self, routes=solution)
            return optimized
        except NotSolvable as error:
            return error.args[0]
        
        
class OrderOptimized(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Órden", related_name="optimized")
    routes = models.TextField(verbose_name="Rutas Optimizadas")

    def __str__(self) -> str:
        return f"{self.order.commodity} - {self.order.ship_from} to {self.order.ship_to}"

    @cached_property
    def to_text(self):
        solutions = self.routes.split(";")
        
        for i in range(0, len(solutions), 4):
            route = Route.objects.filter(
                Q(source__province=solutions[i+2]) & Q(destination__province=solutions[i+3])
            ).first()
            
        print(route)
        
        return ""
    
    def to_list(self):
        icons = {
            "AI": "bi bi-truck",
            "RA": "bi bi-train-front-fill",
            "TR": "bi bi-airplane-fill",
            "SE": "bi bi-water"
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