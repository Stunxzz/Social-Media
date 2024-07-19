from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from posts.views import UserPostListView, CreateAlbumView, UploadImageView, AlbumDetailView, AlbumDeleteView, \
    AddCommentView, AddEmoticonView, ImageDetailView, SendFriendRequestView, FriendRequestsView, \
    AcceptFriendRequestView, RejectFriendRequestView, FriendsListView, AddEmotIconComments, GetReactionsView, \
    GetCommentReactionsView, GetPostReactionCountView, AddPostEmoticonView, CommentEmoticonCountView, \
    PostEmoticonCountView, ImgEmoticonCountView, MakeProfilePictureView

urlpatterns = ([
                   path('', UserPostListView.as_view(), name='profile_dashboard'),
                   path('create-album/', CreateAlbumView.as_view(), name='create_album'),
                   path('upload-image/', UploadImageView.as_view(), name='upload_image'),
                   path('album/<int:album_id>/', AlbumDetailView.as_view(), name='album_detail'),
                   path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
                   path('image/comment/add/', AddCommentView.as_view(), name='add_comment'),
                   path('image/emoticon/add/', AddEmoticonView.as_view(), name='add_emoticon'),
                   path('comment/emoticon/add/', AddEmotIconComments.as_view(), name='add_comment_emoticon'),
                   path('image/<int:image_id>/', ImageDetailView.as_view(), name='image_detail'),
                   path('send-friend-request/<int:user_id>/', SendFriendRequestView.as_view(),
                        name='send_friend_request'),
                   path('get_comment_reactions/', GetCommentReactionsView.as_view(), name='get_comment_reactions'),
                   path('friend_requests/', FriendRequestsView.as_view(), name='friend_requests'),
                   path('accept_friend_request/<int:request_id>/', AcceptFriendRequestView.as_view(),
                        name='accept_friend_request'),
                   path('reject_friend_request/<int:request_id>/', RejectFriendRequestView.as_view(),
                        name='reject_friend_request'),
                   path('friends/', FriendsListView.as_view(), name='friends_list'),
                   path('get_post_reaction_count/', GetPostReactionCountView.as_view(), name='get_post_reaction_count'),
                   path('add_post_emoticon/', AddPostEmoticonView.as_view(), name='add_post_emoticon'),
                   path('get_comment_emoticon_count/<int:pk>/', CommentEmoticonCountView.as_view(),
                        name='get_comment_emoticon_count'),
                   path('get_post_emoticon_count/<int:pk>/', PostEmoticonCountView.as_view(),
                        name='get_post_emoticon_count'),
                   path('get_img_emoticon_count/<int:pk>/', ImgEmoticonCountView.as_view(),
                        name='get_img_emoticon_count'),
                   path('get_reactions/', GetReactionsView.as_view(), name='get_reactions'),
                   path('make_profile_picture/', MakeProfilePictureView.as_view(), name='profile_pic'),

               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
