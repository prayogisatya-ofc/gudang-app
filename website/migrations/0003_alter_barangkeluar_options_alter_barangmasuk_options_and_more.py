# Generated by Django 4.0.3 on 2022-04-09 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_barang_options_alter_barangkeluar_waktu_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='barangkeluar',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='barangmasuk',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='barang',
            name='fungsi',
            field=models.TextField(blank=True),
        ),
    ]