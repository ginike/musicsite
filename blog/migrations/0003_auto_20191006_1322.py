# Generated by Django 2.1.7 on 2019-10-06 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191006_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requesting',
            old_name='your_names',
            new_name='your_name',
        ),
    ]
