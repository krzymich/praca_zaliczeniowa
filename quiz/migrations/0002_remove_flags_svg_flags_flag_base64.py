# Generated by Django 4.1.7 on 2023-03-13 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flags',
            name='svg',
        ),
        migrations.AddField(
            model_name='flags',
            name='flag_base64',
            field=models.BinaryField(null=True),
        ),
    ]