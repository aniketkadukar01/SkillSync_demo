# Generated by Django 5.1.6 on 2025-02-25 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_user_type_user_type_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/user_pictures/'),
        ),
    ]
