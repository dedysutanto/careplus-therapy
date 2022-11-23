# Generated by Django 4.1.2 on 2022-11-23 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_students_call_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='students',
            options={'ordering': ['call_name'], 'verbose_name': 'siswa', 'verbose_name_plural': 'siswa'},
        ),
        migrations.AddField(
            model_name='students',
            name='pin',
            field=models.CharField(default='1810', max_length=4, verbose_name='PIN'),
        ),
    ]
