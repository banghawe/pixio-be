from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .views import PlanViewSet, SubscriptionViewSet, DetectionViewSet

urlpatterns = [
    path('plan', PlanViewSet.as_view({
        'get': 'list',
    })),
    path('subscription', SubscriptionViewSet.as_view({
        'post': 'create',
    })),
    path('subscription/<str:user_id>', SubscriptionViewSet.as_view({
        'get': 'retrieve',
    })),
    path('detection/<str:username>', DetectionViewSet.as_view({
        'get': 'list',
        'post': 'upload',
    })),
    path('detection/<str:username>/<int:detection_id>', DetectionViewSet.as_view({
        'get': 'retrieve',
        'patch': 'detect',
    })),
    path('detection/<int:detection_id>/progress/<str:task_id>', DetectionViewSet.as_view({
        'get': 'progress',
    })),
    path('docs/', TemplateView.as_view(
        template_name='api-docs.html',
    ), name='api-docs'),
]
