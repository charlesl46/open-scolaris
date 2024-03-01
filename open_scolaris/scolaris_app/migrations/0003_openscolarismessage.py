# Generated by Django 4.2.7 on 2024-03-01 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scolaris_app', '0002_alter_class_subjects_taken'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenScolarisMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('content', models.TextField(max_length=1000)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('recipients', models.ManyToManyField(related_name='os_messages_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]