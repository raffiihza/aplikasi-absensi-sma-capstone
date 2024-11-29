from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Class, Lesson, Student, AttendanceGuru, Schedule, AttendanceSiswa, Agenda
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.db.models import Q
from datetime import date, datetime
from django.urls import reverse

# Mapping untuk jadwal absensi siswa dari Inggris ke Indonesia
DAY_MAPPING = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
}


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
def logout_view(request):
    logout(request)
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

# Controller Siswa

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def manage_students(request):
    """
    Halaman index untuk melihat daftar siswa.
    """
    
    students = Student.objects.select_related('id_kelas').all()
    context = {'students': students}
    return render(request, 'students/manage_students.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def add_student(request):
    """
    Tambah siswa baru.
    """

    if request.method == 'POST':
        nisn = request.POST['nisn']
        id_kelas = request.POST['id_kelas']
        nama = request.POST['nama']
        gender = request.POST['gender']

        if Student.objects.filter(nisn=nisn).exists():
            messages.error(request, 'Siswa dengan NISN ini sudah ada.')
            return redirect('add_student')

        Student.objects.create(
            nisn=nisn,
            id_kelas_id=id_kelas,
            nama=nama,
            gender=gender,
        )
        messages.success(request, 'Siswa berhasil ditambahkan.')
        return redirect('manage_students')

    classes = Class.objects.all()
    context = {'classes': classes}
    return render(request, 'students/add_student.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def edit_student(request, student_id):
    """
    Edit siswa yang ada.
    """

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.nisn = request.POST['nisn']
        student.id_kelas_id = request.POST['id_kelas']
        student.nama = request.POST['nama']
        student.gender = request.POST['gender']
        student.save()
        messages.success(request, 'Siswa berhasil diperbarui.')
        return redirect('manage_students')

    classes = Class.objects.all()
    context = {'student': student, 'classes': classes}
    return render(request, 'students/edit_student.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def delete_student(request, student_id):
    """
    Hapus siswa berdasarkan ID.
    """

    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, 'Siswa berhasil dihapus.')
    return redirect('manage_students')

# Controller absensi guru

@login_required
def manage_attendance_guru(request):
    user = User.objects.get(id=request.session.get('user_id'))
    
    # Apakah begini?
    # Jika role-nya adalah Tata Usaha atau Kepala Sekolah, bisa lihat semua absensi
    # Guru hanya bisa melihat absensi mereka sendiri
    # if request.session.get('role') == 'Guru':
    #     attendance_records = AttendanceGuru.objects.filter(id_guru_id=request.session['user_id']).order_by('-tanggal')
    # else:
    #     attendance_records = AttendanceGuru.objects.all().order_by('-tanggal')
        
    attendance_records = AttendanceGuru.objects.filter(id_guru_id=request.session['user_id']).order_by('-tanggal')    
    context = {
        'attendance_records': attendance_records,
        'user': user
        }
    return render(request, 'attendance_guru/manage_attendance_guru.html', context)

@login_required
def add_attendance_guru(request):
    user = User.objects.get(id=request.session.get('user_id'))
    
    if request.method == 'POST':
        id_guru = request.session['user_id']
        status = request.POST['status']
        bukti = request.FILES.get('bukti', None)

        AttendanceGuru.objects.create(
            id_guru_id=id_guru,
            tanggal=date.today(),
            status=status,
            bukti=bukti,
        )
        messages.success(request, 'Absensi guru berhasil ditambahkan.')
        return redirect('manage_attendance_guru')

    context = {
        'user': user,
        'date': datetime.now()
        }
    return render(request, 'attendance_guru/add_attendance_guru.html', context)

# Controller Jadwal

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def manage_schedule(request):
    schedules = Schedule.objects.all()
    context = {
        'schedules': schedules,
    }
    return render(request, 'schedule/manage_schedule.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def add_schedule(request):
    if request.method == 'POST':
        id_lesson = request.POST.get('id_lesson')
        id_class = request.POST.get('id_class')
        id_guru = request.POST.get('id_guru')
        hari = request.POST.get('hari')
        jam_mulai = request.POST.get('jam_mulai')
        durasi = request.POST.get('durasi')
        # agenda_kelas = request.POST.get('agenda_kelas')

        Schedule.objects.create(
            id_lesson_id=id_lesson,
            id_class_id=id_class,
            id_guru_id=id_guru,
            hari=hari,
            jam_mulai=jam_mulai,
            durasi=durasi,
            # agenda_kelas=agenda_kelas
        )
        return redirect('manage_schedule')
    
    lessons = Lesson.objects.all()
    classes = Class.objects.all()
    all_users = User.objects.all()
    context = {'lessons': lessons, 'classes': classes, 'all_users': all_users}
    return render(request, 'schedule/add_schedule.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.id_lesson_id = request.POST.get('id_lesson')
        schedule.id_class_id = request.POST.get('id_class')
        schedule.id_guru_id = request.POST.get('id_guru')
        schedule.hari = request.POST.get('hari')
        schedule.jam_mulai = request.POST.get('jam_mulai')
        schedule.durasi = request.POST.get('durasi')
        # schedule.agenda_kelas = request.POST.get('agenda_kelas')
        schedule.save()
        return redirect('manage_schedule')
    
    lessons = Lesson.objects.all()
    classes = Class.objects.all()
    all_users = User.objects.all()
    context = {'schedule': schedule, 'lessons': lessons, 'classes': classes, 'all_users': all_users}
    return render(request, 'schedule/edit_schedule.html', context)

@role_required(['Tata Usaha', 'Kepala Sekolah'])
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return redirect('manage_schedule')

# Controller absensi siswa

@login_required
def manage_absensi_siswa(request):
    user = User.objects.get(id=request.session.get('user_id'))
    schedules = []
    selected_date = request.GET.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    if selected_date:
        # Filter jadwal berdasarkan hari dari tanggal yang dipilih
        day_name = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%A")
        day_name = DAY_MAPPING.get(day_name, "")
        schedules_awal = Schedule.objects.filter(id_guru_id=request.session['user_id'])
        schedules = schedules_awal.filter(hari=day_name)

    context = {
        "schedules": schedules,
        "selected_date": selected_date,
        "user": user
    }
    return render(request, "absensi_siswa/manage_absensi.html", context)

# EDIT ABSENSI SISWA TIDAK TERPAKAI!!!!
# @login_required
# def edit_absensi_siswa(request, schedule_id):
#     user = User.objects.get(id=request.session.get('user_id'))
#     schedule = get_object_or_404(Schedule, id=schedule_id)
#     students = Student.objects.filter(id_kelas=schedule.id_class)
#     attendance_data = {
#         att.id_siswa.id: att.status
#         for att in AttendanceSiswa.objects.filter(id_schedule=schedule)
#     }
    
#     if request.method == "POST":
#         for student in students:
#             status = request.POST.get(f"status_{student.id}")
#             attendance, created = AttendanceSiswa.objects.update_or_create(
#                 id_siswa=student,
#                 id_schedule=schedule,
#                 defaults={"status": status},
#             )
#         return redirect("manage_absensi_siswa")
    
#     context = {
#         "schedule": schedule,
#         "students": students,
#         "attendance_data": attendance_data,
#         "user": user
#     }
#     return render(request, "absensi_siswa/edit_absensi.html", context)

@login_required
def kelola_agenda_absensi(request, schedule_id, tanggal):
    user = User.objects.get(id=request.session.get('user_id'))
    # Ambil data Schedule berdasarkan ID
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if schedule.id_guru_id != request.session['user_id']:
        return redirect('manage_absensi_siswa')
    
    # Cek apakah sudah ada Agenda untuk tanggal tersebut
    agenda = Agenda.objects.filter(id_schedule=schedule, tanggal=tanggal).first()

    # Ambil siswa dari kelas yang terkait dengan jadwal
    students = Student.objects.filter(id_kelas=schedule.id_class)
    students_with_status = None
    
    # Ambil data absensi siswa jika agenda sudah ada
    # attendance_data = {}
    list_status = []
    if agenda:
        attendance_records = AttendanceSiswa.objects.filter(id_agenda=agenda)
        attendance_records_count = attendance_records.count()
        students_count = students.count()
        leftover_count = 0
        if attendance_records_count < students_count:
            leftover_count = students_count - attendance_records_count
        
        for record in attendance_records:
            # attendance_data[record.id_siswa.id] = record.status
            list_status.append(record.status)
            
        if leftover_count != 0:
            for _ in range(leftover_count):
                list_status.append("Kosong")
            
    else:
        for student in students:
            list_status.append("Kosong")
        
    students_with_status = list(zip(students, list_status))

    if request.method == "POST":
        # Simpan Agenda
        isi_agenda = request.POST.get("isi_agenda")
        if not agenda:
            agenda = Agenda.objects.create(id_schedule=schedule, tanggal=tanggal, isi_agenda=isi_agenda)
        else:
            agenda.isi_agenda = isi_agenda
            agenda.save()

        # Simpan Absensi Siswa
        for student in students:
            status = request.POST.get(f"status_{student.id}")
            attendance, created = AttendanceSiswa.objects.get_or_create(
                id_agenda=agenda, id_siswa=student
            )
            attendance.status = status
            attendance.save()

        return redirect(f"{reverse('manage_absensi_siswa')}?date={tanggal}")  # Sesuaikan dengan URL halaman absensi

    context = {
        "schedule": schedule,
        "tanggal": tanggal,
        "agenda": agenda,
        "students": students,
        # "attendance_data": attendance_data,
        "user": user,
        "list_status": list_status,
        "students_with_status": students_with_status
    }
    return render(request, "absensi_siswa/kelola_absensi.html", context)