# Generated by Django 4.2.13 on 2024-07-18 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_remove_profilepicture_uploaded_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepicture',
            name='image',
            field=models.ImageField(upload_to='profile_pictures/'),
        ),
    ]