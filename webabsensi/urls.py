from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('kelas/', views.manage_classes, name='manage_classes'),
    path('kelas/tambah/', views.add_class, name='add_class'),
    path('kelas/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('kelas/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('mapel/', views.manage_lessons, name='manage_lessons'),
    path('mapel/tambah/', views.add_lesson, name='add_lesson'),
    path('mapel/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path('mapel/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('guru/', views.manage_guru, name='manage_guru'),
    path('guru/tambah/', views.add_guru, name='add_guru'),
    path('guru/edit/<int:id>/', views.edit_guru, name='edit_guru'),
    path('guru/delete/<int:id>/', views.delete_guru, name='delete_guru'),
    path('guru/reset-password/<int:id>/', views.reset_password_guru, name='reset_password_guru'),
    path('siswa/', views.manage_students, name='manage_students'),
    path('siswa/add/', views.add_student, name='add_student'),
    path('siswa/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('siswa/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('absensi_guru/', views.manage_attendance_guru, name='manage_attendance_guru'),
    path('absensi_guru/tambah/', views.add_attendance_guru, name='add_attendance_guru'),
]