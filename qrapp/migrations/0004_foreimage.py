# Generated by Django 5.0 on 2024-02-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrapp', '0003_remove_qrcode_attendance_qrcode_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='dumps/')),
            ],
        ),
    ]