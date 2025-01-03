# Generated by Django 5.1.3 on 2024-11-29 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nama_kelas", models.CharField(max_length=50, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nama_pelajaran", models.CharField(max_length=50, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nip", models.CharField(max_length=20, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("nama", models.CharField(max_length=50)),
                (
                    "gender",
                    models.CharField(
                        choices=[("L", "Laki-laki"), ("P", "Perempuan")], max_length=1
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Tata Usaha", "Tata Usaha"),
                            ("Guru", "Guru"),
                            ("Kepala Sekolah", "Kepala Sekolah"),
                        ],
                        max_length=20,
                    ),
                ),
                ("no_telepon", models.CharField(max_length=15)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "hari",
                    models.CharField(
                        choices=[
                            ("Senin", "Senin"),
                            ("Selasa", "Selasa"),
                            ("Rabu", "Rabu"),
                            ("Kamis", "Kamis"),
                            ("Jumat", "Jumat"),
                        ],
                        max_length=10,
                    ),
                ),
                ("jam_mulai", models.TimeField()),
                ("durasi", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.class",
                    ),
                ),
                (
                    "id_lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.lesson",
                    ),
                ),
                (
                    "id_guru",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Agenda",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tanggal", models.DateField()),
                ("isi_agenda", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.schedule",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nisn", models.CharField(max_length=20, unique=True)),
                ("nama", models.CharField(max_length=50)),
                (
                    "gender",
                    models.CharField(
                        choices=[("L", "Laki-laki"), ("P", "Perempuan")], max_length=1
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_kelas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.class",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceSiswa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Hadir", "Hadir"),
                            ("Sakit", "Sakit"),
                            ("Izin", "Izin"),
                            ("Alfa", "Alfa"),
                        ],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_agenda",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.agenda",
                    ),
                ),
                (
                    "id_siswa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceGuru",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tanggal", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Hadir", "Hadir"),
                            ("Sakit", "Sakit"),
                            ("Izin", "Izin"),
                            ("Cuti", "Cuti"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "bukti",
                    models.FileField(blank=True, null=True, upload_to="bukti_absensi/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id_guru",
                    models.ForeignKey(
                        limit_choices_to={"role": "Guru"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webabsensi.user",
                    ),
                ),
            ],
        ),
    ]
