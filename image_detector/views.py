from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer

class PlanViewSet(viewsets.ViewSet):
  def list(self, request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)

    return Response(serializer.data)

class SubscriptionViewSet(viewsets.ViewSet):
  def retrieve(self, request, user_id=None):
    subscription = Subscription.objects.get(username=user_id)
    serializer = SubscriptionSerializer(subscription)

    return Response(serializer.data)

  def create(self, request):
    #subscription = Subscription.objects.get(username=user_id)

    serializer = SubscriptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

