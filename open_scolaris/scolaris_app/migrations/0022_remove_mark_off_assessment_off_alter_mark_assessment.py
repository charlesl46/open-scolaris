# Generated by Django 5.0 on 2023-12-22 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0021_alter_subject_teachers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='off',
        ),
        migrations.AddField(
            model_name='assessment',
            name='off',
            field=models.SmallIntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='mark',
            name='assessment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='scolaris_app.assessment'),
        ),
    ]