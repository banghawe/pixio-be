from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Plan, Subscription, Detection
from django.contrib.auth.models import User


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'


class UploadImageSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(
        required=True,
        error_messages={"required": "image is required"}
    )

    class Meta:
        model = Detection
        fields = ("id", "img", "subs_id", "created_by", "created_at")


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(User.objects.all(), "Email must be unique")]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, error_messages={'required': 'first_name is required'})
    last_name = serializers.CharField(required=True, error_messages={'required': 'last_name is required'})

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "first_name", "last_name")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "password didn't match!"})

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )

            user.set_password(validated_data["password"])
            user.save()

            Subscription.objects.create(
                username_id=user.id,
                plan_id=1,
                status=True
            )

        return user



