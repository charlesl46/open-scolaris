# Generated by Django 5.0 on 2023-12-20 00:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0015_homework_marked_as_done_alter_homework_due_course_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='marked_as_done',
        ),
        migrations.CreateModel(
            name='HomeworkCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scolaris_app.homework')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'S'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
