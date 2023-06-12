from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet

from apps.feedbacks.models import Feedback, Rating
from apps.feedbacks.serializers import FeedbackSerializer, RatingSerializer


class FeedBackViewSet(ModelViewSet):
    """Вьюсет для отзывов."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class RatingViewSet(ModelViewSet):
    """Вьюсет для рейтингов."""

    queryset = Rating.objects.all().annotate(score=Avg('feedbacks__rating'))
    serializer_class = RatingSerializer

