from django.test import TestCase
from apps.core.models.route import Route
from apps.core.models.location import Location
from apps.core.models.constants import TravelMode, Province, PortType


class RouteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        source = Location.objects.create(province=Province.LA_HABANA, port_type=PortType.AIRPORT)
        destination = Location.objects.create(province=Province.PINAR_DEL_RIO, port_type=PortType.PORT)
        Route.objects.create(source=source, destination=destination, travel_mode=TravelMode.AIR, transit_time=48)

    def test_source_label(self):
        route = Route.objects.get(id=1)
        field_label = route._meta.get_field('source').verbose_name
        self.assertEqual(field_label, 'Lugar de origen')

    def test_destination_label(self):
        route = Route.objects.get(id=1)
        field_label = route._meta.get_field('destination').verbose_name
        self.assertEqual(field_label, 'Lugar de destino')

    def test_travel_mode_label(self):
        route = Route.objects.get(id=1)
        field_label = route._meta.get_field('travel_mode').verbose_name
        self.assertEqual(field_label, 'Modo de Viaje')

    def test_object_name_is_source_destination(self):
        route = Route.objects.get(id=1)
        expected_object_name = f"{route.source} --> {route.destination}"
        self.assertEqual(expected_object_name, str(route))