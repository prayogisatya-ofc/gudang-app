# Generated by Django 4.0.3 on 2022-04-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_barangkeluar_options_alter_barangmasuk_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangkeluar',
            name='pengambil',
            field=models.CharField(max_length=100),
        ),
    ]