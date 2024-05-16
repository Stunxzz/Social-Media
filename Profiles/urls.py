from django.urls import path
from Profiles.views import (CreateProfileView, CustomLoginView, UserProfileCreateView,
                            UserPostListView)


urlpatterns = [
    path('register/', CreateProfileView.as_view(), name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('profile_info/', UserProfileCreateView.as_view(), name='profile_info'),
    path('profile_dashboard/', UserPostListView.as_view(), name='profile_dashboard')

]
