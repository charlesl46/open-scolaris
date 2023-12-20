# Generated by Django 5.0 on 2023-12-19 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_role'),
        ('scolaris_app', '0008_course_class_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='class_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scolaris_app.class'),
        ),
    ]