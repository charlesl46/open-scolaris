# Generated by Django 5.0 on 2023-12-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0024_alter_mark_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='mark',
            field=models.FloatField(null=True),
        ),
    ]