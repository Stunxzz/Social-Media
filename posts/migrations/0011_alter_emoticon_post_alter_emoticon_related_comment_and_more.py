# Generated by Django 4.2.13 on 2024-06-03 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_alter_userprofile_comments_alter_userprofile_posts_and_more'),
        ('posts', '0010_remove_emoticon_related_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoticon',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_comment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.comment'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_profile_img',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.profilepicture'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_user_img',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.userimage'),
        ),
    ]