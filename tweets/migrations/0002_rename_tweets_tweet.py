# Generated by Django 5.2 on 2025-04-28 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tweets',
            new_name='Tweet',
        ),
    ]
