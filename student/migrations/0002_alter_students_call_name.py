# Generated by Django 3.2.6 on 2022-10-26 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='call_name',
            field=models.CharField(max_length=50, verbose_name='Nama Panggilan'),
        ),
    ]
