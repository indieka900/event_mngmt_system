# Generated by Django 5.2.4 on 2025-07-25 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='key_words',
            field=models.TextField(blank=True, null=True),
        ),
    ]
