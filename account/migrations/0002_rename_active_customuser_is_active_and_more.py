# Generated by Django 5.1.1 on 2024-09-18 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='admin',
            new_name='is_staff',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='staff',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
