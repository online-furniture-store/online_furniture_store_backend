from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

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

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class StorehouseViewSet(viewsets.ModelViewSet):
    queryset = Storehouse.objects.all()
    serializer_class = StorehouseSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrdersReadSerializer
        return OrdersWriteSerializer

    @action(detail=True, methods=['post'])
    def payment_confirmation(self, request, **kwargs):
        if request.method == 'POST':
            order = get_object_or_404(Orders, id=kwargs['pk'])
            order.paid = True
            order.save(update_fields=['paid'])
            return Response({'detail': 'Заказ успешно оплачен.'}, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
