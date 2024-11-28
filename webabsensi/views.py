from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Class, Lesson
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

# Create your views here.

# Decorator dan wrapper
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

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, 'Anda harus login terlebih dahulu.')
                return redirect('login')
            
            user = User.objects.get(id=request.session['user_id'])
            if user.role not in allowed_roles:
                return render(request, '403.html', {'message': 'Anda tidak memiliki izin untuk mengakses halaman ini.'})
            
            request.user = user  # Tambahkan user ke request agar dapat digunakan di template
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Controller auth

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

# Controller Profile
@login_required
def profile(request):
    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        action = request.POST.get('action')

        # Update Data Diri
        if action == 'update_profile':
            user.nama = request.POST.get('nama')
            user.gender = request.POST.get('gender')
            user.no_telepon = request.POST.get('no_telepon')
            user.save()
            messages.success(request, 'Data diri berhasil diperbarui.')
            return redirect('profile')

        # Update Password
        elif action == 'update_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Validasi Password
            if not check_password(current_password, user.password):
                messages.error(request, 'Password saat ini salah.')
            elif new_password != confirm_password:
                messages.error(request, 'Password baru tidak cocok.')
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password berhasil diperbarui.')
                return redirect('profile')

    return render(request, 'profile.html', {'user': user})

# Controller Class

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def manage_classes(request):
    """
    Halaman index untuk melihat daftar kelas.
    """
    
    classes = Class.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'classes': classes,
        'user': user,
    }
    return render(request, 'classes/manage_classes.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def add_class(request):
    """
    Tambah kelas baru.
    """

    if request.method == 'POST':
        nama_kelas = request.POST.get('nama_kelas')
        if nama_kelas:
            Class.objects.create(nama_kelas=nama_kelas)
            return redirect('manage_classes')
        else:
            return render(request, 'classes/add_class.html', {'error': 'Nama kelas harus diisi.'})

    return render(request, 'classes/add_class.html')

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def edit_class(request, class_id):
    """
    Edit kelas yang ada.
    """

    kelas = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        nama_kelas = request.POST.get('nama_kelas')
        if nama_kelas:
            kelas.nama_kelas = nama_kelas
            kelas.save()
            return redirect('manage_classes')
        else:
            return render(request, 'classes/edit_class.html', {'kelas': kelas, 'error': 'Nama kelas harus diisi.'})

    return render(request, 'classes/edit_class.html', {'kelas': kelas})

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def delete_class(request, class_id):
    """
    Hapus kelas berdasarkan ID.
    """

    kelas = get_object_or_404(Class, id=class_id)
    kelas.delete()
    return redirect('manage_classes')

# Controller Lesson

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def manage_lessons(request):
    """
    Halaman index untuk melihat daftar mapel.
    """
    
    lessons = Lesson.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'lessons': lessons,
        'user': user,
    }
    return render(request, 'lessons/manage_lessons.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def add_lesson(request):
    """
    Tambah mapel baru.
    """

    if request.method == 'POST':
        nama_pelajaran = request.POST.get('nama_pelajaran')
        if nama_pelajaran:
            Lesson.objects.create(nama_pelajaran=nama_pelajaran)
            return redirect('manage_lessons')
        else:
            return render(request, 'lessons/add_lesson.html', {'error': 'Nama mapel harus diisi.'})

    return render(request, 'lessons/add_lesson.html')

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def edit_lesson(request, lesson_id):
    """
    Edit mapel yang ada.
    """

    pelajaran = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        nama_pelajaran = request.POST.get('nama_pelajaran')
        if nama_pelajaran:
            pelajaran.nama_pelajaran = nama_pelajaran
            pelajaran.save()
            return redirect('manage_lessons')
        else:
            return render(request, 'lessons/edit_lesson.html', {'pelajaran': pelajaran, 'error': 'Nama pelajaran harus diisi.'})

    return render(request, 'lessons/edit_lesson.html', {'pelajaran': pelajaran})

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def delete_lesson(request, lesson_id):
    """
    Hapus mapel berdasarkan ID.
    """

    pelajaran = get_object_or_404(Lesson, id=lesson_id)
    pelajaran.delete()
    return redirect('manage_lessons')

# Controller Guru

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def manage_guru(request):
    """
    Halaman index untuk melihat daftar guru.
    """
    
    guru_list = User.objects.filter(role="Guru").order_by('-created_at')
    return render(request, 'guru/manage_guru.html', {'guru_list': guru_list})

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def add_guru(request):
    """
    Tambah guru baru.
    """

    if request.method == 'POST':
        nip = request.POST.get('nip')
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        no_telepon = request.POST.get('no_telepon')

        if User.objects.filter(nip=nip).exists():
            messages.error(request, "NIP sudah terdaftar!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah terdaftar!")
        else:
            hashed_password = make_password(password)
            User.objects.create(
                nip=nip, email=email, password=hashed_password, nama=nama,
                gender=gender, role="Guru", no_telepon=no_telepon
            )
            return redirect('manage_guru')
    return render(request, 'guru/add_guru.html')

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def edit_guru(request, id):
    """
    Edit guru yang ada.
    """

    guru = get_object_or_404(User, id=id, role="Guru")
    if request.method == 'POST':
        guru.nip = request.POST.get('nip')
        guru.email = request.POST.get('email')
        guru.nama = request.POST.get('nama')
        guru.gender = request.POST.get('gender')
        guru.no_telepon = request.POST.get('no_telepon')
        guru.save()
        return redirect('manage_guru')
    return render(request, 'guru/edit_guru.html', {'guru': guru})

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def delete_guru(request, id):
    """
    Hapus guru berdasarkan ID.
    """

    guru = get_object_or_404(User, id=id, role="Guru")
    guru.delete()
    return redirect('manage_guru')

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def reset_password_guru(request, id):
    """
    Reset password guru berdasarkan ID.
    """

    # Fetch the Guru by ID
    guru = get_object_or_404(User, id=id, role='Guru')
    
    # Set default password and hash it
    default_password = '123'
    guru.password = make_password(default_password)
    guru.save()

    return redirect('manage_guru')