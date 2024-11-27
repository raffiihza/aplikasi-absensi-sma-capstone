from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('kelas/', views.manage_classes, name='manage_classes'),
    path('kelas/tambah/', views.add_class, name='add_class'),
    path('kelas/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('kelas/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('mapel/', views.manage_lessons, name='manage_lessons'),
    path('mapel/tambah/', views.add_lesson, name='add_lesson'),
    path('mapel/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path('mapel/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
]