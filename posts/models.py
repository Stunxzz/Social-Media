from django.db import models
from django.conf import settings

from Profiles.models import UserProfile


class ProfilePicture(models.Model):
    user_profile = models.OneToOneField('Profiles.UserProfile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Album(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='album_pictures/', default='album_pictures/default.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_cover_image(self):
        last_photo = self.images.order_by('-uploaded_at').first()
        if last_photo:
            return last_photo.image.url
        return self.cover_image.url

    def __str__(self):
        return self.title


class UserImage(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='user_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"


class Post(models.Model):
    user_profile = models.ForeignKey('Profiles.UserProfile', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE , blank=True, null=True)
    user_profile = models.ForeignKey('Profiles.UserProfile', on_delete=models.CASCADE)
    pictures = models.ForeignKey('UserImage', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Emoticon(models.Model):
    LIKE = 'like'
    HEART = 'heart'
    SMILE = 'smile'
    RAGE = 'rage'

    EMOTICON_CHOICES = [
        (LIKE, 'Like'),
        (HEART, 'Heart'),
        (SMILE, 'Smile'),
        (RAGE, 'Rage'),
    ]

    emoticon_type = models.CharField(max_length=10, choices=EMOTICON_CHOICES)
    related_user_img = models.ForeignKey(UserImage, on_delete=models.CASCADE, blank=True, null=True)
    related_profile_img = models.ForeignKey(ProfilePicture, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    related_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)


# class Emoticon(models.Model):
#     LIKE = 'like'
#     HEART = 'heart'
#     SMILE = 'smile'
#     RAGE = 'rage'
#
#     EMOTICON_CHOICES = [
#         (LIKE, 'Like'),
#         (HEART, 'Heart'),
#         (SMILE, 'Smile'),
#         (RAGE, 'Rage'),
#     ]
#
#     emoticon_type = models.CharField(max_length=10, choices=EMOTICON_CHOICES)
#     related_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='emoticon')
#     related_post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='emoticon', blank=True, null=True)
#     related_comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='emoticon', blank=True, null=True)
#     related_image = models.OneToOneField(UserImage, on_delete=models.CASCADE, related_name='emoticon', blank=True, null=True)
#     related_profile_img = models.OneToOneField(ProfilePicture, on_delete=models.CASCADE, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.emoticon_type} - {self.related_user.first_name}"

