import sys

from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Plan, Subscription, Detection
from .serializers import PlanSerializer, SubscriptionSerializer, DetectionSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class PlanViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request: Request) -> Response:
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)

        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ViewSet):
    @staticmethod
    def retrieve(request: Request, user_id: str = None) -> Response:
        try:
            user = User.objects.get(username=user_id)
            subscription = Subscription.active_objects.get(username=user.id)
            serializer = SubscriptionSerializer(subscription)

            return Response(serializer.data)
        except ObjectDoesNotExist as ex:
            print(ex)
            return Response({"message": "User has not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            print(sys.exc_info()[0])
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create(request: Request) -> Response:
        try:
            username = request.data["username"]
            plan = request.data["plan"]
            user = User.objects.filter(username=username).first()
            data = request.data

            if user is None:
                return Response({"message": "user has not found"}, status=status.HTTP_400_BAD_REQUEST)

            subs = Subscription.active_objects.get(username=user.id)

            if subs is not None:
                if subs.plan.id == plan:
                    return Response(
                        {"message": "You have already subscribe to this plan"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    subs.deactivate()

            data["username"] = user.id

            serializer = SubscriptionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            print(sys.exc_info())
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetectionViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def list(request: Request, username: str) -> Response:
        try:
            user = User.objects.get(username=username)
            detections = Detection.objects.filter(created_by=user.id)
            serializer = DetectionSerializer(detections, many=True)

            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "User has not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            print(sys.exc_info())
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def retrieve(request: Request, username: str, detection_id: int) -> Response:
        try:
            detection = Detection.objects.get(pk=detection_id)
            serializer = DetectionSerializer(detection)

            return Response(serializer.data)
        except Detection.DoesNotExist:
            return Response({"message": "Detection has not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def upload(request: Request, username: str) -> Response:
        try:
            serializer = DetectionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            print(sys.exc_info())
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def detect(request: Request, username: str, detection_id: int) -> Response:
        pass

    @staticmethod
    def progress(request: Request, detection_id: int) -> Response:
        pass
