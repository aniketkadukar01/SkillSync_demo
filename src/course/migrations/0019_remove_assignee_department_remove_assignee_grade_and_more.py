# Generated by Django 5.1.6 on 2025-02-27 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_question_is_lesson_alter_lesson_media_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignee',
            name='department',
        ),
        migrations.RemoveField(
            model_name='assignee',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='assignee',
            name='type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_lesson',
        ),
    ]
