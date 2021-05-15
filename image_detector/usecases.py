import datetime
import os

from celery.result import AsyncResult
from django.conf import settings
from django.utils import timezone
from typing import Any

from .models import Plan, Subscription, Detection
from .tasks import detect_image
from django.contrib.auth.models import User

from .serializers import DetectionSerializer, UploadImageSerializer, SubscriptionSerializer
from rest_framework.exceptions import NotFound, ValidationError


class DetectionUseCase:
    SECONDS_IN_A_DAY = 1 * 24 * 60 * 60

    def __init__(self, username):
        self.username = username
        self.__get_info(username)

    def __get_info(self, username):
        try:
            self.subscription = Subscription.active_objects.get(username__username=username)
        except Subscription.DoesNotExist:
            raise NotFound("User has not subscribe to any plan", 404)

    def __has_detection_quota_left(self) -> bool:
        if self.subscription.plan_id == 1:
            detection = Detection.objects.filter(created_by__username=self.username).order_by('-created_at')
            print(detection[0].created_at, timezone.now())
            if detection is not None \
                    and (timezone.now() - detection[0].created_at).total_seconds() < self.SECONDS_IN_A_DAY:
                return False

        return True

    def __has_subscribe_plan(self) -> bool:
        return self.subscription is not None

    def validate(self) -> bool:
        return self.__has_subscribe_plan() and self.__has_detection_quota_left()

    def create_detection_transaction(self, data) -> DetectionSerializer.data:
        serializer = UploadImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

    def execute(self, data) -> Any:
        if not self.validate():
            raise ValidationError('Please check your subscription plan and detection quota left')
        else:
            return self.create_detection_transaction(data)


class DetectImageUseCase:
    def __init__(self, detection_id):
        self.detection_id = detection_id

    def get(self) -> Any:
        try:
            detection = Detection.objects.get(pk=self.detection_id)
            serializer = DetectionSerializer(detection)

            return serializer.data
        except Detection.DoesNotExist:
            raise NotFound("Detection has not found", 404)

    @staticmethod
    def get_list(username: str) -> Any:
        try:
            detections = Detection.objects.filter(created_by__username=username)
            serializer = DetectionSerializer(detections, many=True)

            return serializer.data
        except Detection.DoesNotExist:
            raise NotFound("Detection has not found", 404)

    def detect(self) -> Any:
        detection = Detection.objects.get(pk=self.detection_id)
        img_path = os.path.join(settings.BASE_DIR, detection.img.path)

        return detect_image.delay(img_path, self.detection_id)

    def get_progress(self, task_id: str) -> Any:
        task = AsyncResult(task_id)
        data = task.result

        data = {"message": task.state} if not data else data

        if data == 1:
            detection = Detection.objects.get(pk=self.detection_id)
            serializer = DetectionSerializer(detection)
            data = serializer.data

        return data


class SubscriptionUseCase:
    def __init__(self, username):
        self.username = username

    def get(self):
        if self.__has_already_subscribe():
            serializer = SubscriptionSerializer(self.subscription)

            return serializer.data

        raise NotFound("User does not subscribe to any plan", 404)

    def __has_already_subscribe(self) -> bool:
        try:
            self.subscription = Subscription.active_objects.get(username__username=self.username)

            return True
        except Subscription.DoesNotExist:
            return False

    def __can_update_subscription(self, data):
        return not (self.subscription.plan_id == data.plan_id)

    def create(self, data: SubscriptionSerializer.data) -> SubscriptionSerializer.data:
        if self.__has_already_subscribe():
            if self.__can_update_subscription():
                self.subscription.deactivate()
            else:
                raise ValidationError("You have already subscribe to this plan", 400)

        user = User.objects.filter(username=self.username).first()

        if user is None:
            raise NotFound("User has not found", 404)

        data["username"] = user.id
        serializer = SubscriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data
