# Generated by Django 4.2.11 on 2024-05-06 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_first_name_alter_user_last_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["id"]},
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="ActivationKey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.UUIDField(editable=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activation_key",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
