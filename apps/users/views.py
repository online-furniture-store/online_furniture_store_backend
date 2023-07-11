from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.serializers import OrderReadSerializer
from apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'my_orders':
            return OrderReadSerializer
        return UserSerializer

    @action(detail=False)
    def my_orders(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        if not current_password or not new_password:
            return Response(
                {'error': 'Требуется указать текущий и новый пароль, заполните поля current_password и new_password'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(current_password):
            return Response({'error': 'Неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
