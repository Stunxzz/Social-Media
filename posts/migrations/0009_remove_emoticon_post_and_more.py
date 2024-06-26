# Generated by Django 4.2.13 on 2024-06-03 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_alter_userprofile_comments_alter_userprofile_posts_and_more'),
        ('posts', '0008_emoticon_related_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emoticon',
            name='post',
        ),
        migrations.RemoveField(
            model_name='emoticon',
            name='related_user_img',
        ),
        migrations.AddField(
            model_name='emoticon',
            name='related_image',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emoticon', to='posts.userimage'),
        ),
        migrations.AddField(
            model_name='emoticon',
            name='related_post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emoticon', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_comment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emoticon', to='posts.comment'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_profile_img',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.profilepicture'),
        ),
        migrations.AlterField(
            model_name='emoticon',
            name='related_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='emoticon', to='Profiles.userprofile'),
        ),
    ]
