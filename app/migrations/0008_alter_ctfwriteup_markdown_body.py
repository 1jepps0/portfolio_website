# Generated by Django 5.1.3 on 2024-11-26 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_ctfwriteup_image_ctfimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctfwriteup',
            name='markdown_body',
            field=models.FileField(upload_to='media'),
        ),
    ]
