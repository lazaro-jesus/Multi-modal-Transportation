from django.test import TestCase
from apps.core.models.route import Route
from apps.core.models.location import Location
from apps.core.models.constants import TravelMode, Province, PortType


class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Location.objects.create(province=Province.LA_HABANA, port_type=PortType.AIRPORT)

    def test_province_label(self):
        location = Location.objects.get(id=1)
        field_label = location._meta.get_field('province').verbose_name
        self.assertEqual(field_label, 'Provincia')

    def test_port_type_label(self):
        location = Location.objects.get(id=1)
        field_label = location._meta.get_field('port_type').verbose_name
        self.assertEqual(field_label, 'Tipo de puerto')

    def test_object_name_is_province_port_type(self):
        location = Location.objects.get(id=1)
        expected_object_name = f'{location.province} {location.port_type}'
        self.assertEqual(expected_object_name, str(location))