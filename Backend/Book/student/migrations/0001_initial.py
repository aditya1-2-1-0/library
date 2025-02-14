# Generated by Django 5.1.2 on 2025-02-05 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='Available', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_name', models.CharField(max_length=50)),
                ('roll_no', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField()),
                ('submission_date', models.DateField()),
                ('fine_per_day', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fine_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(default='Issued', max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]
