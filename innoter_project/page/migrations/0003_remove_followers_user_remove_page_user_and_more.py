# Generated by Django 4.2.5 on 2023-10-10 13:35

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("page", "0002_remove_followers_user_id_followers_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="followers",
            name="user",
        ),
        migrations.RemoveField(
            model_name="page",
            name="user",
        ),
        migrations.AddField(
            model_name="followers",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="page",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
