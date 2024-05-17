from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .managers import CustomUserManager

MAX_NAME = 255
WORKING_PLACE_CHAR = 255

class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField('auth.Group', related_name='profile_groups', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='profile_permissions',
        blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def has_user_profile(self):
        return hasattr(self, 'userprofile')

    def get_absolute_url(self):
        return reverse('profile_info')

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=MAX_NAME)
    last_name = models.CharField(max_length=MAX_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    working_place = models.CharField(max_length=WORKING_PLACE_CHAR, blank=True)
    posts = models.ManyToManyField('Post', blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    comments = models.ManyToManyField('Comment', blank=True)

class ProfilePicture(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/blank-profil.webp')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserImage(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pictures = models.ManyToManyField(UserImage, blank=True)
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
    related_user_img = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    related_profile_img = models.ForeignKey(ProfilePicture, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    related_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
