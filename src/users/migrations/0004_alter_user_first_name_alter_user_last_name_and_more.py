# Generated by Django 4.2.11 on 2024-04-15 13:37

from django.db import migrations, models

import users.enums


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("senior", "Senior"),
                    ("junior", "Junior"),
                    ("admin", "Admin"),
                ],
                default=users.enums.Role["JUNIOR"],
                max_length=15,
            ),
        ),
    ]
