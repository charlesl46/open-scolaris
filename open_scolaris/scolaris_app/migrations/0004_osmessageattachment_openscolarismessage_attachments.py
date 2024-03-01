# Generated by Django 4.2.7 on 2024-03-01 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolaris_app', '0003_openscolarismessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='OSMessageAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
            ],
        ),
        migrations.AddField(
            model_name='openscolarismessage',
            name='attachments',
            field=models.ManyToManyField(blank=True, to='scolaris_app.osmessageattachment'),
        ),
    ]
