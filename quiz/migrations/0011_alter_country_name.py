# Generated by Django 4.1.7 on 2023-03-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_country_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]