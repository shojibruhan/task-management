# Generated by Django 4.2.18 on 2025-01-18 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_task_project"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="task",
            name="assigned_to",
            field=models.ManyToManyField(to="tasks.employee"),
        ),
    ]
