# Generated by Django 5.2.4 on 2025-07-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("equipements", "0005_materiel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="materiel",
            name="date_mise_en_service",
        ),
        migrations.AddField(
            model_name="materiel",
            name="date_service",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date de service"
            ),
        ),
    ]
