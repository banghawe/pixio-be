from django.contrib import admin
from .models import Plan, Subscription, Detection

admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Detection)
