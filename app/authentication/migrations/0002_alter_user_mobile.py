# Generated by Django 5.1.5 on 2025-02-03 00:26

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="mobile",
            field=models.CharField(
                blank=True, max_length=20, null=True, unique=True
            ),
        ),
    ]
