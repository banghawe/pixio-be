# Generated by Django 2.2.19 on 2021-04-14 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_detector', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='plan_id',
            new_name='plan',
        ),
    ]
