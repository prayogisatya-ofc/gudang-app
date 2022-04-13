from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    userRole = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('officer', 'Officer'),
    ]
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    nama = models.CharField(max_length=100)
    role = models.CharField(choices=userRole, max_length=7)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.nama

class Barang(models.Model):
    nama = models.CharField(max_length=200)
    fungsi = models.TextField(blank=True)
    pemasok = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']
    
    def get_stok(self, *args, **kwargs):
        subMasuk = 0
        subKeluar = 0
        masuks = BarangMasuk.objects.filter(barang=self.id)
        keluars = BarangKeluar.objects.filter(barang=self.id)
        for masuk in masuks:
            subMasuk += masuk.stok

        for keluar in keluars:
            subKeluar += keluar.stok

        totalStok = subMasuk - subKeluar
        return totalStok
    
    stok = property(get_stok)

    def __str__(self):
        return self.nama

class BarangMasuk(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    stok = models.IntegerField(default=0)
    penerima = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu = models.DateField(auto_now_add=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.barang.nama

class BarangKeluar(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    stok = models.IntegerField(default=0)
    pengambil = models.CharField(max_length=100)
    waktu = models.DateField(auto_now_add=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.barang.nama