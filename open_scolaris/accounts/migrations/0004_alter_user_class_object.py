# Generated by Django 5.0 on 2023-12-20 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_class_object'),
        ('scolaris_app', '0017_remove_class_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='class_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scolaris_app.class'),
        ),
    ]
