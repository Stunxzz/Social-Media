# Generated by Django 4.2.13 on 2024-07-02 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_comment_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilepicture',
            name='uploaded_at',
        ),
    ]
