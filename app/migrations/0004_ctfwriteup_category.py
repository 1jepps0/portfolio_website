# Generated by Django 5.1.3 on 2024-11-25 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_ctfwriteup_body_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctfwriteup',
            name='category',
            field=models.CharField(default='No Category', max_length=50),
            preserve_default=False,
        ),
    ]
