# Generated by Django 5.1.6 on 2025-02-28 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0020_useranswer_userscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='user_answer',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
