# Generated by Django 4.2.16 on 2025-02-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_remove_otp_is_verified_otp_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='otp',
            name='expires_at',
            field=models.DateTimeField(),
        ),
    ]
