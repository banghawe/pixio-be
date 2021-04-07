from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Plan(models.Model):
  name = models.CharField(max_length=500)
  price = models.DecimalField(max_digits=24, decimal_places=2)
  status = models.BooleanField(default=True)

  def __str__(self):
    return self.name

class Subscription(models.Model):
  username = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  plan_id = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
  start_at = models.DateField(default=timezone.now)
  end_at = models.DateField(default=timezone.now)
  status = status = models.BooleanField(default=True)

class Detection(models.Model):
  subs_id = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING)
  img_path = models.TextField()
  result_img_path = models.TextField(blank=True)
  result_percentage = models.DecimalField(max_digits=5, decimal_places=2)
  created_at = models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
