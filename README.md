# aplikasi-absensi-sma-capstone

## Cara install Django
1. Clone repository ke lokal (atau kalau malas, bisa pakai GitHub Codespaces)
2. Buka terminal di directory repository dan ketik `pip install -r requirements.txt`
3. Untuk membaca database SQLite, buka menggunakan software seperti HeidiSQL atau bisa juga memakai ekstensi VSCode

## Cara run aplikasi
1. Untuk sekarang tidak perlu migrasi karena file database tersimpan di SQLite
2. Untuk menjalankan web server, ketik `python manage.py runserver`

## Hierarki directory

Note: Kenapa ada dua folder `aplikasiabsensi` (untuk setting project) dan `webabsensi` (untuk code aplikasi sesungguhnya), yo ndak tau kok tanya saya. Dari Django memang dipisah buat project sama app. Terus karena nama `aplikasiabsensi` udah terlanjur jadi nama project-nya, jadinya buat nama app-nya `webabsensi`.

```
manage.py
aplikasiabsensi/    : directory setting project
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
webabsensi/         : directory aplikasi sesungguhnya
    __init__.py
    admin.py
    apps.py
    migrations/     : directory file migrasi
    models.py       : file model
    tests.py        : file test
    urls.py         : file route
    views.py        : file view (dan controller?)
```