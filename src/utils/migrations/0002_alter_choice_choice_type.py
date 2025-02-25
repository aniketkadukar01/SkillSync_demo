# Generated by Django 5.1.6 on 2025-02-25 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_type',
            field=models.CharField(choices=[('user', 'User'), ('answer', 'Answer'), ('assignee', 'Assignee'), ('status', 'Status'), ('gender', 'Gender'), ('designation', 'Designation')], max_length=255),
        ),
    ]
