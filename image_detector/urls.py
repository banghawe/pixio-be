from django.contrib import admin
from django.urls import path

from .views import PlanViewSet, SubscriptionViewSet

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
]
