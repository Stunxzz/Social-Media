from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from Profiles.models import UserProfile
from posts.models import ProfilePicture
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


def chat_room(request):

    return render(request, 'chat/chat_room.html')



def friends_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    friends = user_profile.friends.all()
    friends_data = []
    for friend in friends:
        profile_picture = ProfilePicture.objects.get(user_profile=friend)
        friends_data.append({
            'id': friend.id,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
            'image_url': profile_picture.image.url if profile_picture else None,
        })
    return JsonResponse(friends_data, safe=False)


def chat(request):
    user_profile = request.user.userprofile
    friends = user_profile.friends.all()
    context = {
        'user_profile': user_profile,
        'friends': friends
    }
    return render(request, 'chat/chat.html', context)