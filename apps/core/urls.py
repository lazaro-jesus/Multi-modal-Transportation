from django.urls import path

from .views import (
    HomeView,
    
    OrderCreateView,
    OrderListView,
    OrderUpdateView,
    OrderDeleteView,
    OrderOptimizeView,
    
    RouteCreateView,
    RouteListView,
    RouteUpdateView,
    RouteDeleteView,
    RouteSearchView
)


app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Orders
    path("order-create/", OrderCreateView.as_view(), name="order-create"),
    path("order-list/", OrderListView.as_view(), name="order-list"),
    path("order-update/<int:pk>/", OrderUpdateView.as_view(), name="order-update"),
    path("order-delete/<int:pk>/", OrderDeleteView.as_view(), name="order-delete"),
    path("order-optimize/<int:pk>/", OrderOptimizeView.as_view(), name="order-optimize"),
    
    # Routes
    path("route-create/", RouteCreateView.as_view(), name="route-create"),
    path("route-list/", RouteListView.as_view(), name="route-list"),
    path("route-update/<int:pk>/", RouteUpdateView.as_view(), name="route-update"),
    path("route-delete/<int:pk>/", RouteDeleteView.as_view(), name="route-delete"),
    path("route-search/", RouteSearchView.as_view(), name="route-search"),
]