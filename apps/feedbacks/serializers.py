from rest_framework import serializers

from apps.feedbacks.models import Feedback, Rating
from apps.users.serializers import UserSerializer
from apps.product.serializers import ShortProductSerializer


class FeedbackSerializer(serializers.Serializer):
    """Сериалайзер для модели Feedback."""
    user = UserSerializer(read_only=True)
    product = ShortProductSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['user',
                  'product',
                  'feedback',
                  'rating']


class RatingSerializer(serializers.Serializer):
    """Сериалайзер для модели Rating."""

    class Meta:
        model = Rating
        fields = ['product',
                  'count',
                  'score']
