import random

from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Route, Location, Province, PortType, TravelMode


class Command(BaseCommand):
    help = "Crea datos manualmente para pruebas"

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        # Crea instancias de Location
        provinces = Province.labels
        port_types = PortType.labels
        locations_to_create = [{"province": province, "port_type": port_type} for province in provinces for port_type in port_types]
        locations: list[Location] = []
        
        for location_data in locations_to_create:
            province = location_data["province"]
            port_type = location_data["port_type"]

            location, _ = Location.objects.get_or_create(
                    province=province,
                    port_type=port_type
                )
            locations.append(location)
            
        travel_mode = dict(zip(PortType.labels, TravelMode.values))

        # Crea instancias de Route
        for i in range(50):
            source = random.choice(locations)
            destination = random.choice(locations)
            route, _ = Route.objects.get_or_create(
                source=source,
                destination=destination,
                container_size=1000,
                carrier="Empresa",
                travel_mode=travel_mode[source.port_type],
                fixed_freight_cost=0,
                handling_cost=0,
                bunker_fuel_cost=0,
                documentation_cost=0,
                equipment_cost=0,
                extra_cost=0,
                warehouse_cost=0,
                transit_duty=0.0,
                custom_clearance_time=0,
                handling_time=0,
                extra_time=0,
                transit_time=random.choice([24, 48, 72]),
                monday=True,
                tuesday=True,
                wednesday=True,
                thursday=True,
                friday=True,
                saturday=True,
                sunday=True
            )

        self.stdout.write(self.style.SUCCESS("Datos creados exitosamente"))
