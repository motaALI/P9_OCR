# Generated by Django 4.1.4 on 2023-02-25 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_profile_profileimg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profileimg',
            new_name='image',
        ),
    ]