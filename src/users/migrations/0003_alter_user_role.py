# Generated by Django 4.2.11 on 2024-04-12 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_date_joined_user_groups_user_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(max_length=15),
        ),
    ]
