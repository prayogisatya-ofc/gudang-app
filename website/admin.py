from django.contrib import admin
from . import models as db

@admin.register(db.Barang)
class BarangAdmin(admin.ModelAdmin):
    pass

@admin.register(db.BarangMasuk)
class BarangMasukAdmin(admin.ModelAdmin):
    pass

@admin.register(db.BarangKeluar)
class BarangKeluarAdmin(admin.ModelAdmin):
    pass

@admin.register(db.User)
class UserAdmin(admin.ModelAdmin):
    pass