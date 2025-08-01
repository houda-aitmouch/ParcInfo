# Generated by Django 5.2.4 on 2025-07-26 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="PermissionMetier",
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
                ("nom", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("icone", models.CharField(default="📋", max_length=10)),
                (
                    "permissions_techniques",
                    models.ManyToManyField(
                        to="auth.permission", verbose_name="Permissions techniques"
                    ),
                ),
            ],
            options={
                "verbose_name": "Permission métier",
                "verbose_name_plural": "Permissions métier",
                "ordering": ["nom"],
            },
        ),
        migrations.CreateModel(
            name="GroupeMetier",
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
                ("nom", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "groupe_django",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.group",
                        verbose_name="Groupe Django",
                    ),
                ),
                (
                    "permissions_metier",
                    models.ManyToManyField(
                        to="users.permissionmetier", verbose_name="Permissions métier"
                    ),
                ),
            ],
            options={
                "verbose_name": "Groupe métier",
                "verbose_name_plural": "Groupes métier",
                "ordering": ["nom"],
            },
        ),
    ]
