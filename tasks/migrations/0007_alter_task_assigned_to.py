# Generated by Django 4.2.18 on 2025-01-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0006_alter_taskdetail_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="assigned_to",
            field=models.ManyToManyField(related_name="tasks", to="tasks.employee"),
        ),
    ]
