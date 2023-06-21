from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from apps.orders.models import Delivery, DeliveryType, Order
from apps.orders.serializers import (
    DeliverySerializer,
    DeliveryTypeSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)

User = get_user_model()


class DeliveryTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для способов доставки."""

    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    """Вьюсет для доставок."""

    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Вьюсет для заказов."""

    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializer
        return OrderWriteSerializer

    @action(detail=True, methods=['post'])
    def payment_confirmation(self, request, **kwargs):
        if request.method == 'POST':
            order = get_object_or_404(Order, id=kwargs['pk'])
            order.paid = True
            order.save(update_fields=['paid'])
            return Response({'detail': 'Заказ успешно оплачен.'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
