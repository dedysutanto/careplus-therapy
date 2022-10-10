# Generated by Django 3.2.6 on 2022-10-10 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('therapist', '0001_initial'),
        ('schedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schedules',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapist.therapists', verbose_name='Therapist'),
        ),
        migrations.AddField(
            model_name='schedules',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
