# Generated by Django 4.1.4 on 2023-02-25 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0002_alter_review_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profileimg",
            field=models.ImageField(
                default="blank-profile-picture.png", upload_to="profile_images/"
            ),
        ),
    ]
