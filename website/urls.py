from .program import login, dashboard, barang, barangMasuk, barangKeluar, petugas, akunSaya
from django.urls import path

urlpatterns = [
    path('login/', login.controller, name='loginPage'),
    path('logout/', dashboard.controller, name='handleLogout'),

    path('', dashboard.controller, name="dashboard"),
    path('barang/', barang.controller, name="viewBarang"),
    path('barang/hapus/', barang.hapus, name="handleHapusBarang"),
    path('barang/print/', barang.printData, name="viewPrintBarang"),
    path('barang/export/', barang.exportData, name="exportData"),

    path('barang-masuk/', barangMasuk.controller, name="viewBarangMasuk"),
    path('barang-masuk/tambah-baru/', barangMasuk.tambah, name="handleTambahBarangMasukBaru"),
    path('barang-masuk/update-barang/', barangMasuk.update, name="handleUbahBarangMasukBaru"),
    path('barang-masuk/hapus-barang/', barangMasuk.hapus, name="handleHapusBarangMasukBaru"),
    path('barang-masuk/print/<str:start>/<str:end>/', barangMasuk.printData, name="handlePrintBarangMasuk"),
    path('barang-masuk/export/<str:start>/<str:end>/', barangMasuk.exportData, name="handleExportBarangMasuk"),

    path('barang-keluar/', barangKeluar.controller, name="viewBarangKeluar"),
    path('barang-keluar/update-barang/', barangKeluar.update, name="handleUbahBarangKeluar"),
    path('barang-keluar/hapus-barang/', barangKeluar.hapus, name="handleHapusBarangKeluar"),
    path('barang-keluar/print/<str:start>/<str:end>/', barangKeluar.printData, name="handlePrintBarangKeluar"),
    path('barang-keluar/export/<str:start>/<str:end>/', barangKeluar.exportData, name="handleExportBarangKeluar"),

    path('petugas/', petugas.controller, name="viewPetugas"),
    path('petugas/update-petugas/', petugas.update, name="handleUbahPetugas"),
    path('petugas/hapus-petugas/', petugas.hapus, name="handleHapusPetugas"),

    path('akun-saya/', akunSaya.controller, name="viewAkunSaya"),
]