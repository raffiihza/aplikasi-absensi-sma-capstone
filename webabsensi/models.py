from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = [
        ('Tata Usaha', 'Tata Usaha'),
        ('Guru', 'Guru'),
        ('Kepala Sekolah', 'Kepala Sekolah'),
    ]
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    
    nip = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    nama = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    no_telepon = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama


class Class(models.Model):
    nama_kelas = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_kelas


class Student(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    nisn = models.CharField(max_length=20, unique=True)
    id_kelas = models.ForeignKey(Class, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama


class Lesson(models.Model):
    nama_pelajaran = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_pelajaran


class Schedule(models.Model):
    HARI_CHOICES = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
    ]

    id_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    id_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    id_guru = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Guru'})
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    durasi = models.IntegerField()  # dalam menit
    agenda_kelas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_lesson.nama_pelajaran} - {self.id_class.nama_kelas}"

class AttendanceGuru(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Sakit', 'Sakit'),
        ('Izin', 'Izin'),
        ('Cuti', 'Cuti'),
    ]

    id_guru = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Guru'})
    tanggal = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    bukti = models.FileField(upload_to='bukti_absensi/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_guru.nama} - {self.tanggal}"


class AttendanceSiswa(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Alfa', 'Alfa'),
    ]

    id_siswa = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_siswa.nama} - {self.status}"
