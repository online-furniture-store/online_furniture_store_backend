from django.contrib import admin

from apps.feedbacks.models import Feedback, Rating


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'product', 'rating')
    search_fields = ('product', 'user',)
    list_filter = ('product', 'user',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'count', 'score')
    search_fields = ('product',)
    list_filter = ('product',)
