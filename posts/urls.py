from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from posts.views import UserPostListView, CreateAlbumView, UploadImageView, AlbumDetailView, AlbumDeleteView, \
    AddCommentView, AddEmoticonView, ImageDetailView

urlpatterns = ([
                   path('', UserPostListView.as_view(), name='profile_dashboard'),
                   path('create-album/', CreateAlbumView.as_view(), name='create_album'),
                   path('upload-image/', UploadImageView.as_view(), name='upload_image'),
                   path('album/<int:album_id>/', AlbumDetailView.as_view(), name='album_detail'),
                   path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
                   path('image/comment/add/', AddCommentView.as_view(), name='add_comment'),
                   path('image/emoticon/add/', AddEmoticonView.as_view(), name='add_emoticon'),
                   path('image/<int:image_id>/', ImageDetailView.as_view(), name='image_detail'),

               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
