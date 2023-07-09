from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    birthday = serializers.DateField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birthday', 'phone']

        extra_kwargs = {'url': {'view_name': 'api:user-detail', 'lookup_field': 'pk'}}
