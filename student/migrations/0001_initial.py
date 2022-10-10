# Generated by Django 3.2.6 on 2022-10-10 05:11

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nama Lengkap')),
                ('call_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nama Panggilan')),
                ('gender', models.CharField(choices=[('M', 'Laki-Laki'), ('F', 'Perempuan')], default='M', max_length=3, verbose_name='Jenis Kelamin')),
                ('dob', models.DateField(verbose_name='Tanggal Lahir')),
                ('pob', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tempat Lahir')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('religion', models.CharField(blank=True, choices=[('CHRISTIAN', 'Kristen'), ('CATHOLIC', 'Katholik'), ('ORTHODOX', 'Orthodox'), ('ISLAM', 'Islam'), ('HINDU', 'Hindu'), ('BUDDHA', 'Budha')], default='CHRISTIAN', max_length=50, null=True, verbose_name='Agama')),
                ('school_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nama Sekolah')),
                ('biological_child', models.BooleanField(default=True, verbose_name='Apakah Anak Kandung')),
            ],
            options={
                'verbose_name': 'siswa',
                'verbose_name_plural': 'siswa',
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='Sibling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('older_sibling_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nama Kakak')),
                ('younger_sibling_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nama Adik')),
                ('is_normal', models.BooleanField(default=False, verbose_name='Apakah ada riwayat keterlambatan tumbuh kembang pada kakak/adik ')),
                ('student', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_sibling', to='student.students')),
            ],
            options={
                'verbose_name': 'kakak/Adik',
                'verbose_name_plural': 'kakak/Adik',
                'db_table': 'sibling',
            },
        ),
        migrations.CreateModel(
            name='ParentMother',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nama Ibu')),
                ('dob', models.DateField(verbose_name='Tanggal Lahir')),
                ('pob', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tempat Lahir')),
                ('education', models.CharField(choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA/SMK'), ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3')], default='S1', max_length=10, verbose_name='Pendidikan Terakhir')),
                ('occupation', models.CharField(choices=[('TIDAK_BEKERJA', 'Tidak Bekerja'), ('PNS', 'PNS/ASN'), ('TNI_POLRI', 'TNI/POLRI'), ('PEGAWAI_SWASTA', 'Pegawai Swasta'), ('WIRAUSAHA', 'Wira Usaha')], default='PEGAWAI_SWASTA', max_length=20, verbose_name='Pekerjaan')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telpon Rumah/Kantor')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nomor HP')),
                ('religion', models.CharField(blank=True, choices=[('CHRISTIAN', 'Kristen'), ('CATHOLIC', 'Katholik'), ('ORTHODOX', 'Orthodox'), ('ISLAM', 'Islam'), ('HINDU', 'Hindu'), ('BUDDHA', 'Budha')], default='CHRISTIAN', max_length=50, null=True, verbose_name='Agama')),
                ('student', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_mother', to='student.students')),
            ],
            options={
                'verbose_name': 'Ibu',
                'verbose_name_plural': 'Ibu',
                'db_table': 'parent_mother',
            },
        ),
        migrations.CreateModel(
            name='ParentFather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nama Ayah')),
                ('dob', models.DateField(verbose_name='Tanggal Lahir')),
                ('pob', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tempat Lahir')),
                ('education', models.CharField(choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA/SMK'), ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3')], default='S1', max_length=10, verbose_name='Pendidikan')),
                ('occupation', models.CharField(choices=[('TIDAK_BEKERJA', 'Tidak Bekerja'), ('PNS', 'PNS/ASN'), ('TNI_POLRI', 'TNI/POLRI'), ('PEGAWAI_SWASTA', 'Pegawai Swasta'), ('WIRAUSAHA', 'Wira Usaha')], default='PEGAWAI_SWASTA', max_length=20, verbose_name='Pekerjaan')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telpon Rumah/Kantor')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nomor HP')),
                ('religion', models.CharField(blank=True, choices=[('CHRISTIAN', 'Kristen'), ('CATHOLIC', 'Katholik'), ('ORTHODOX', 'Orthodox'), ('ISLAM', 'Islam'), ('HINDU', 'Hindu'), ('BUDDHA', 'Budha')], default='CHRISTIAN', max_length=50, null=True, verbose_name='Agama')),
                ('student', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_father', to='student.students')),
            ],
            options={
                'verbose_name': 'ayah',
                'verbose_name_plural': 'ayah',
                'db_table': 'parent_father',
            },
        ),
    ]
