# Generated by Django 3.2.6 on 2022-10-11 02:35

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data_support', '0002_packages'),
        ('student', '0004_students_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_support.packages', verbose_name='Paket Yang Diambil'),
        ),
        migrations.AddField(
            model_name='students',
            name='package_session',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_support.packages', verbose_name='Paket Yang Diambil')),
                ('student', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_package', to='student.students')),
            ],
            options={
                'verbose_name': 'Paket Siswa',
                'verbose_name_plural': 'Paket Siswa',
                'db_table': 'student_package',
            },
        ),
    ]