# Generated by Django 5.0 on 2024-03-07 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scolaris_app", "0004_osmessageattachment_openscolarismessage_attachments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="openscolarismessage",
            name="content",
            field=models.TextField(max_length=2000),
        ),
    ]
