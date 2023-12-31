# Generated by Django 5.0 on 2023-12-17 17:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0002_class'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='code',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='teachers',
        ),
        migrations.AddField(
            model_name='course',
            name='date_begin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='date_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20)),
                ('teachers', models.ManyToManyField(limit_choices_to={'role': 'T'}, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
