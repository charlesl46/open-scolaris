# Generated by Django 5.0 on 2023-12-19 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0008_course_class_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
