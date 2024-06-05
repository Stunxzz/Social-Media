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
    posts = models.ManyToManyField('posts.Post', blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    comments = models.ManyToManyField('posts.Comment', blank=True)

    def send_friend_request(self, to_user_profile):
        try:
            friend_request = FriendRequest.objects.get(from_user=self, to_user=to_user_profile)
            if friend_request.status == 'pending':
                friend_request.cancel()
                return 'Friend request cancelled.'
            elif friend_request.status == 'rejected':
                friend_request.status = 'pending'
                friend_request.save()
                return 'Friend request re-sent.'
        except FriendRequest.DoesNotExist:
            FriendRequest.objects.create(from_user=self, to_user=to_user_profile)
            return 'Friend request sent.'

    def remove_friend(self, friend):
        self.friends.remove(friend.userprofile)
        friend.userprofile.friends.remove(self)





class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('cancelled', 'cancelled')
    ]

    from_user = models.ForeignKey(UserProfile, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.status = 'accepted'
        self.save()
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)
        self.delete()

    def reject(self):
        self.status = 'rejected'
        self.delete()

    def cancel(self):
        self.status = 'cancelled'
        self.delete()