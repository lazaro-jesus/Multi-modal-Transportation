from django.test import TestCase
from apps.core.models.order import Order, OrderOptimized
from apps.core.models.location import Location
from apps.core.models.constants import Province, PortType
from datetime import date

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ship_from = Location.objects.create(province=Province.LA_HABANA, port_type=PortType.AIRPORT)
        ship_to = Location.objects.create(province=Province.PINAR_DEL_RIO, port_type=PortType.PORT)
        order = Order.objects.create(
            ship_from=ship_from,
            ship_to=ship_to,
            commodity="Test Commodity",
            value=100,
            volume=10,
            required_delivery_date=date.today(),
        )
        OrderOptimized.objects.create(order=order, routes="Test Route")
        
    def test_ship_from_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('ship_from').verbose_name
        self.assertEqual(field_label, 'Lugar de origen')

    def test_ship_to_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('ship_to').verbose_name
        self.assertEqual(field_label, 'Lugar de destino')

    def test_commodity_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('commodity').verbose_name
        self.assertEqual(field_label, 'Mercancía')

    def test_order_optimized_routes_label(self):
        order_optimized = OrderOptimized.objects.get(id=1)
        field_label = order_optimized._meta.get_field('routes').verbose_name
        self.assertEqual(field_label, 'Rutas Optimizadas')

    def test_order_optimized_solved_label(self):
        order_optimized = OrderOptimized.objects.get(id=1)
        field_label = order_optimized._meta.get_field('solved').verbose_name
        self.assertEqual(field_label, 'Solucionado')
        
    def test_order_str_method(self):
        order = Order.objects.get(id=1)
        expected_str = f"Test Commodity - {order.ship_from} to {order.ship_to}"
        self.assertEqual(str(order), expected_str)

    def test_location_to_calculate_property(self):
        location = Location.objects.create(province=Province.LA_HABANA, port_type=PortType.PORT)
        self.assertEqual(location.to_calculate, "La Habana Puerto")
        
