# Generated by Django 4.1.7 on 2023-03-18 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_rename_country_name_flags_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translations',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.language'),
        ),
    ]