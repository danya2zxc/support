# Generated by Django 4.2.11 on 2024-05-21 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_alter_issue_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
