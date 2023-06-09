from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

# from rest_framework.decorators import action
# from rest_framework.response import Response
from apps.orders.models import Delivery, DeliveryMethod, Orders, Storehouse
from apps.orders.serializers import (
    DeliveryMethodSerializer,
    DeliverySerializer,
    OrdersReadSerializer,
    OrdersWriteSerializer,
    StorehouseSerializer,
)

User = get_user_model()


class DeliveryMethodViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrdersReadSerializer
        return OrdersWriteSerializer


class StorehouseViewSet(viewsets.ModelViewSet):
    queryset = Storehouse.objects.all()
    serializer_class = StorehouseSerializer

    # def get_serializer_class(self):
    #     if self.request.method in SAFE_METHODS:
    #         return StorehouseReadSerializer
    #     return StorehouseWriteSerializer
