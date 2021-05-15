from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import PlanViewSet, SubscriptionViewSet, DetectionViewSet, RegisterView

urlpatterns = [
    path('plan', PlanViewSet.as_view({
        'get': 'list',
    })),
    path('subscription', SubscriptionViewSet.as_view({
        'post': 'create',
        'get': 'retrieve',
    })),
    path('detection', DetectionViewSet.as_view({
        'get': 'list',
        'post': 'upload',
    })),
    path('detection/<int:detection_id>', DetectionViewSet.as_view({
        'get': 'retrieve',
        'patch': 'detect',
    })),
    path('detection/<int:detection_id>/progress/<str:task_id>', DetectionViewSet.as_view({
        'get': 'progress',
    })),
    path('docs/', TemplateView.as_view(
        template_name='api-docs.html',
    ), name='api-docs'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('register', RegisterView.as_view(), name='auth_register')
]
