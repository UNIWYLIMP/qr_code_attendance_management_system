# Generated by Django 5.0 on 2024-02-12 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrapp', '0004_foreimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(default='', max_length=250, unique=True, verbose_name='Course Code'),
        ),
    ]