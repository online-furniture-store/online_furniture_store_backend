from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import Order
from apps.orders.serializers import OrderReadSerializer
from apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, serializer_class=OrderReadSerializer)
    def my_orders(self, request):
        queryset = Order.objects.filter(user=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
