from django.contrib import admin
from .models import Location, Route, Order, OrderOptimized


for model in [Location, Route, Order, OrderOptimized]:
    admin.site.register(model)
