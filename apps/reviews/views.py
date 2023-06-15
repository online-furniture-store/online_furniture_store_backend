from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.reviews.models import Rating, Review
from apps.reviews.serializers import RatingSerializer, ReviewSerializer
from common.permisions import IsOwner


class ReviewViewSet(ModelViewSet):
    """Представление  для отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner,)


class RatingViewSet(ReadOnlyModelViewSet):
    """Представление для рейтинга товаров."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
