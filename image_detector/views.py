from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request: Request) -> Response:
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)

        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ViewSet):
    @staticmethod
    def retrieve(request: Request, user_id: str = None) -> Response:
        subscription = Subscription.objects.get(username=user_id)
        serializer = SubscriptionSerializer(subscription)

        return Response(serializer.data)

    @staticmethod
    def create(request: Request) -> Response:
        # subscription = Subscription.objects.get(username=user_id)

        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
