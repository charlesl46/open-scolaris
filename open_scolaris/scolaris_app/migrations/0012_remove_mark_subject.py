# Generated by Django 5.0 on 2023-12-19 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0011_assessment_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='subject',
        ),
    ]