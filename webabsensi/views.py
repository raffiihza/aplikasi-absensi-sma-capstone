from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

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
        if 'user_id' in request.session:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@guest_required
def register(request):
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.POST['nama']
        nip = request.POST['nip']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        gender = request.POST['gender']
        no_telepon = request.POST['no_telepon']
        
        if User.objects.filter(Q(email=email) | Q(nip=nip)).exists():
            messages.error(request, "Email atau NIP sudah terdaftar.")
            return redirect('register')

        # Buat user baru
        hashed_password = make_password(password)
        user = User.objects.create(
            nama=nama,
            nip=nip,
            email=email,
            password=hashed_password,
            role=role,
            gender=gender,
            no_telepon=no_telepon,
        )
        user.save()
        messages.success(request, 'Pendaftaran berhasil. Silakan login.')
        return redirect('login')
    return render(request, 'register.html')

@guest_required
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            # Check password hash
            if check_password(password, user.password):
                # Save user info in session
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, "Email atau password salah.")
        except User.DoesNotExist:
            messages.error(request, "Akun tidak ditemukan.")
            
    return render(request, 'login.html')

@login_required
def logout(request):
    request.session.flush()
    messages.success(request, 'Logout berhasil.')
    return redirect('login')

@login_required
def dashboard(request):
    user = User.objects.get(id=request.session.get('user_id'))
    context = {'user': user}
    return render(request, 'dashboard.html', context)