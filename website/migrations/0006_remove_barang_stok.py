# Generated by Django 4.0.3 on 2022-04-10 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_barangkeluar_waktu_alter_barangmasuk_waktu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barang',
            name='stok',
        ),
    ]
