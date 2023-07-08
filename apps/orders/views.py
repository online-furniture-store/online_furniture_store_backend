import random
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import Delivery, DeliveryType, Order
from apps.orders.serializers import (
    DeliverySerializer,
    DeliveryTypeSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)
from apps.users.serializers import UserSerializer

User = get_user_model()


def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    print(password)  # Здесь будет вызов отправки пароля на почту
    return make_password(password)


class DeliveryTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для способов доставки."""

    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    """Вьюсет для доставок."""

    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrderViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Вьюсет для заказов. Создание заказа либо получение заказов."""

    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializer
        return OrderWriteSerializer

    def create(self, request, *args, **kwargs):
        """Метод создания заказа. Если пользователь аноним - сначала создается запись пользователя."""

        email_data = dict(email=request.data.pop('email'))
        data = request.data
        data['user'] = request.user.pk or self.create_user_pk(email_data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise ValidationError(
                {'product': 'Товары в заказе не могут повторяться. Добавлять товар следует через количество.'}
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def create_user_pk(data):
        """Создает пользователя по данным из формы оформления заказа."""

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(email=data['email'], password=generate_password())
        return user.pk

    @action(detail=True, methods=['post'])
    def payment_confirmation(self, request, pk):
        """Оплата заказа."""

        order = self.get_object()
        order.paid = True
        order.save(update_fields=['paid'])
        return Response({'detail': 'Заказ успешно оплачен.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def save_total_cost(self, request, pk):
        """Сохранение общей стоимости заказа."""

        order = self.get_object()
        order.total_cost = order.order_products.aggregate(Sum('cost'))['cost__sum']
        order.save(update_fields=['total_cost'])
        return Response({'detail': 'Заказ обновлен.'}, status=status.HTTP_201_CREATED)
