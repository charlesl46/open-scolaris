# Generated by Django 4.2.7 on 2024-03-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scolaris_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="class",
            name="subjects_taken",
            field=models.ManyToManyField(blank=True, to="scolaris_app.subject"),
        ),
    ]
