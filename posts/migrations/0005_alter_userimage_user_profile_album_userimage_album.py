# Generated by Django 4.2.13 on 2024-05-21 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_alter_userprofile_comments_alter_userprofile_posts_and_more'),
        ('posts', '0004_alter_profilepicture_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profiles.userprofile'),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profiles.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='userimage',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='posts.album'),
        ),
    ]
