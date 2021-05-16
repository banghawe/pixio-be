from rest_framework import viewsets, status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User

from .models import Plan
from .serializers import PlanSerializer, RegisterSerializer
from .usecases import DetectionUseCase, DetectImageUseCase, SubscriptionUseCase


class PlanViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request: Request) -> Response:
        plans = Plan.active_objects.all()
        serializer = PlanSerializer(plans, many=True)

        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def retrieve(request: Request) -> Response:
        subscription = SubscriptionUseCase(request.user)
        data = subscription.get()

        return Response(data)

    @staticmethod
    def create(request: Request) -> Response:
        subscription = SubscriptionUseCase(request.user)
        data = subscription.create(request.data)

        return Response(data, status=status.HTTP_201_CREATED)


class DetectionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    def list(request: Request) -> Response:
        print(request.user)
        data = DetectImageUseCase.get_list(request.user)

        return Response(data)

    @staticmethod
    def retrieve(request: Request, detection_id: int) -> Response:
        detect_image_use_case = DetectImageUseCase(detection_id)
        data = detect_image_use_case.get()

        return Response(data)

    @staticmethod
    def upload(request: Request) -> Response:
        detection_use_case = DetectionUseCase(request.user)
        data = detection_use_case.execute(request.data)

        return Response(data, status=status.HTTP_201_CREATED)

    @staticmethod
    def detect(request: Request, detection_id: int) -> Response:
        detect_image_use_case = DetectImageUseCase(detection_id)
        result = detect_image_use_case.detect()

        return Response({"message": "detection is on progress", "task_id": result.id})

    @staticmethod
    def progress(request: Request, detection_id: int, task_id: str) -> Response:
        detect_image_use_case = DetectImageUseCase(detection_id)
        data = detect_image_use_case.get_progress(task_id)

        return Response(data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
