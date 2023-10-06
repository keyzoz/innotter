# Generated by Django 4.2.5 on 2023-10-02 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Followers",
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
                ("user_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Page",
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
                ("name", models.CharField(max_length=128, unique=True)),
                ("description", models.TextField()),
                ("image_url", models.URLField(blank=True, null=True)),
                ("user", models.IntegerField()),
                ("is_blocked", models.BooleanField(default=False)),
                ("unblock_date", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True, related_name="followers", to="page.followers"
                    ),
                ),
                ("tags", models.ManyToManyField(related_name="tags", to="page.tag")),
            ],
        ),
        migrations.AddField(
            model_name="followers",
            name="page_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follow_page",
                to="page.page",
            ),
        ),
    ]
