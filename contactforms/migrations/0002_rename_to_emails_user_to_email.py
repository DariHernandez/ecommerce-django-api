# Generated by Django 4.0.4 on 2022-06-14 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactforms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='to_emails',
            new_name='to_email',
        ),
    ]
