# Generated by Django 5.0.1 on 2025-01-16 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=200)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="Jurisdiction",
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
                ("code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Legislation",
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
                ("title", models.CharField(max_length=500)),
                ("description", models.TextField()),
                (
                    "tier",
                    models.CharField(
                        choices=[
                            (1, "Tier 1"),
                            (2, "Tier 2"),
                            ("3H", "Tier 3 High"),
                            ("3L", "Tier 3 Low"),
                        ],
                        max_length=2,
                    ),
                ),
                ("compliance_owner", models.CharField(max_length=200)),
                ("business_owner", models.CharField(max_length=200)),
                ("admin_department", models.CharField(max_length=200)),
                ("administering_body", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_review_date", models.DateField(blank=True, null=True)),
                ("next_review_date", models.DateField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="legislations",
                        to="legislation.category",
                    ),
                ),
                (
                    "jurisdiction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="legislations",
                        to="legislation.jurisdiction",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Legislation",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="LegislationReview",
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
                ("review_date", models.DateField()),
                ("reviewed_by", models.CharField(max_length=200)),
                ("comments", models.TextField(blank=True)),
                (
                    "legislation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="legislation.legislation",
                    ),
                ),
            ],
            options={
                "ordering": ["-review_date"],
            },
        ),
    ]
