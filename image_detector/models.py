import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class ActiveSubsManager(models.Manager):
    def get_queryset(self):
        today = datetime.date.today()
        result = super().get_queryset().filter(status=1).filter(Q(end_at__gte=today) | Q(end_at=None))

        return result


class Plan(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    status = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    start_at = models.DateField(default=timezone.now)
    end_at = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def is_active(self) -> bool:
        today = datetime.date.today()
        return self.status and (self.end_at is None or self.end_at >= today)

    def deactivate(self) -> None:
        self.status = False
        super().save()

    objects = models.Manager()
    active_objects = ActiveSubsManager()

    def __str__(self):
        return f'{self.plan} - {self.is_active()}'


class Detection(models.Model):
    subs_id = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING)
    img = models.ImageField(upload_to="input", null=True, blank=True)
    result_img = models.ImageField(upload_to="result", null=True, blank=True)
    result_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
