from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User as CustomUser

# Create your views here.

# Ada fungsi ini karena tidak pakai Django auth system bawaan
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, 'Anda harus login terlebih dahulu.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@guest_required
def register_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.POST['nama']
        nip = request.POST['nip']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        gender = request.POST['gender']
        no_telepon = request.POST['no_telepon']

        # Buat user baru
        user = CustomUser.objects.create(
            nama=nama,
            nip=nip,
            email=email,
            password=password,
            role=role,
            gender=gender,
            no_telepon=no_telepon,
        )
        user.save()
        messages.success(request, 'Pendaftaran berhasil. Silakan login.')
        return redirect('login')
    return render(request, 'register.html')

@guest_required
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.filter(email=email, password=password).first()
        if user:
            # Simpan session
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            messages.error(request, 'Email atau password salah.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout berhasil.')
    return redirect('login')

@login_required
def dashboard(request):
    user = CustomUser.objects.get(id=request.session.get('user_id'))
    context = {'user': user}
    return render(request, 'dashboard.html', context)