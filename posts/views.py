import json
from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from Profiles.models import UserProfile, FriendRequest
from posts.forms import PostCreationForm, CommentCreationForm, AlbumForm, UserImageForm, EmoticonForm
from posts.models import Post, Comment, Album, Emoticon, UserImage, ProfilePicture
from django.db.models import Q, Prefetch


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        friends = user_profile.friends.all()

        posts = Post.objects.filter(
            Q(user_profile__in=friends) | Q(user_profile=user_profile)
        ).select_related('user_profile').prefetch_related(
            Prefetch('comment_set', queryset=Comment.objects.order_by('-created_at')),
            Prefetch('emoticon_set', queryset=Emoticon.objects.filter(related_comment__isnull=True, related_user_img__isnull=True))
        ).order_by('-created_at')

        user_images = UserImage.objects.filter(
            Q(user_profile__in=friends) | Q(user_profile=user_profile)
        ).select_related('user_profile').prefetch_related(
            Prefetch('emoticon_set', queryset=Emoticon.objects.filter(related_comment__isnull=True)),
            Prefetch('comment_set', queryset=Comment.objects.order_by('-created_at'))
        ).order_by('-uploaded_at')
        post_form = PostCreationForm()
        comment_form = CommentCreationForm()

        context['user_profile'] = user_profile
        context['friends'] = friends
        context['posts'] = posts
        context['user_images'] = user_images
        context['post_form'] = post_form
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        post_form = PostCreationForm(request.POST)
        comment_form = CommentCreationForm(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'post_form' and post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.user_profile = UserProfile.objects.get(user=request.user)
            new_post.save()
            return redirect('profile_dashboard')

        elif form_type == 'comment_form':
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.user_profile = UserProfile.objects.get(user=request.user)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                new_comment.post = post
                new_comment.save()

                return redirect('profile_dashboard')

        elif form_type == 'comment_image_form':
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.user_profile = UserProfile.objects.get(user=request.user)
                image_id = request.POST.get('picture_id')
                image = UserImage.objects.get(id=image_id)
                new_comment.pictures = image
                new_comment.save()

        return self.get(request, *args, **kwargs)


class CommentEmoticonCountView(View):
    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        emoticon_count = comment.emoticon_set.count()
        return JsonResponse({'count': emoticon_count})


class ImgEmoticonCountView(View):
    def get(self, request, pk, *args, **kwargs):
        img = get_object_or_404(UserImage, pk=pk)
        emoticon_count = img.emoticon_set.count()
        return JsonResponse({'count': emoticon_count})


class PostEmoticonCountView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        emoticon_count = post.emoticon_set.count()
        return JsonResponse({'count': emoticon_count})

class CreateAlbumView(View, LoginRequiredMixin):
    form_class = AlbumForm
    template_name = 'create_album.html'

    def get(self, request):
        form = self.form_class()
        user_profile = request.user.userprofile
        albums = Album.objects.filter(user_profile=user_profile)
        context = {
            'form': form,
            'albums': albums,
            'user_profile': user_profile
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.user_profile = request.user.userprofile
            album.save()
            return redirect('create_album')
        user_profile = request.user.userprofile
        albums = Album.objects.filter(user_profile=user_profile)
        return render(request, self.template_name, {'form': form, 'albums': albums})


class UploadImageView(View, LoginRequiredMixin):
    form_class = UserImageForm
    template_name = 'upload_image.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user_profile = request.user.userprofile
            user_image.save()
            return redirect('profile_dashboard')
        return render(request, self.template_name, {'form': form})


class AlbumDetailView(View, LoginRequiredMixin):
    template_name = 'album_detail.html'
    form_class = UserImageForm

    def get(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)
        images = album.images.all()
        user_profile = UserProfile.objects.get(user=self.request.user)
        form = self.form_class()
        comment_form = CommentCreationForm()
        emoticon_form = EmoticonForm()

        context = {
            'album': album,
            'images': images,
            'user_profile': user_profile,
            'form': form,
            'comment_form': comment_form,
            'emoticon_form': emoticon_form,

        }
        return render(request, self.template_name, context)

    def post(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user_profile = request.user.userprofile
            user_image.album = album
            user_image.save()
            return redirect('album_detail', album_id=album.id)
        images = album.images.all()
        return render(request, self.template_name,
                      {'album': album, 'images': images, 'form': form})


class AddCommentView(View, LoginRequiredMixin):
    try:
        def post(self, request):
            data = request.POST

            content = data.get('content')
            user_id = data.get('user_id')
            if data.get('image_id'):
                image_id = data.get('post_id')
                Comment.objects.create(content=content, pictures_id=image_id, user_profile_id=user_id)

            elif data.get('post_id'):
                post_id = data.get('post_id')
                Comment.objects.create(content=content, post_id=post_id, user_profile_id=user_id)
            return JsonResponse({'success': True})

    except Exception as e:
        pass


class GetCommentReactionsView(View):
    def get(self, request):
        comment_id = request.GET.get('comment_id')
        reactions = Emoticon.objects.filter(related_comment_id=comment_id).select_related('related_user')

        reactions_data = [{
            'user_first_name': reaction.related_user.first_name,
            'user_second_name': reaction.related_user.last_name,
            'user_profile_img': reaction.related_user.profilepicture.image.url if reaction.related_user.profilepicture else '',
            'type': reaction.emoticon_type
        } for reaction in reactions]

        return JsonResponse({'success': True, 'reactions': reactions_data})


class GetPostReactionCountView(View):
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        reaction_count = Emoticon.objects.filter(post=post).count()
        return JsonResponse({'success': True, 'reaction_count': reaction_count})


class AddEmotIconComments(View, LoginRequiredMixin):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')
            emoticon_type = data.get('emoticon_type')
            user_id = data.get('user_id')
            existing_emoticon = Emoticon.objects.filter(related_comment_id=comment_id, related_user_id=user_id).first()

            if existing_emoticon:
                if existing_emoticon.emoticon_type == emoticon_type:
                    existing_emoticon.delete()
                else:
                    existing_emoticon.emoticon_type = emoticon_type
                    existing_emoticon.save()
            else:
                Emoticon.objects.create(emoticon_type=emoticon_type, related_user_id=user_id,
                                        related_comment_id=comment_id)

            return JsonResponse({'success': True})
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class AddEmoticonView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            emoticon_type = data.get('emoticon_type')
            user_id = data.get('user_id')

            try:
                user_image = UserImage.objects.get(id=image_id)
                user_profile = UserProfile.objects.get(id=user_id)
            except UserImage.DoesNotExist:
                return JsonResponse({'error': 'Image not found'}, status=404)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            try:
                emoticon = Emoticon.objects.get(
                    related_user_img=user_image,
                    related_user=user_profile
                )

                if emoticon.emoticon_type == emoticon_type:
                    emoticon.delete()
                else:
                    emoticon.emoticon_type = emoticon_type
                    emoticon.save()
            except Emoticon.DoesNotExist:
                Emoticon.objects.create(
                    emoticon_type=emoticon_type,
                    related_user_img=user_image,
                    related_user=user_profile
                )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AlbumDeleteView(DeleteView, LoginRequiredMixin):
    model = Album
    success_url = reverse_lazy('create_album')

    def post(self, request, *args, **kwargs):
        album_id = kwargs['pk']
        album = self.get_object()
        album.delete()
        return HttpResponseRedirect(self.success_url)


class ImageDetailView(View, LoginRequiredMixin):
    def get(self, request, image_id):
        image = get_object_or_404(UserImage, id=image_id)
        comments = Comment.objects.filter(pictures=image)
        emoticons = Emoticon.objects.filter(related_user_img=image)

        emoticon_counts = {'like': 0, 'heart': 0, 'smile': 0, 'rage': 0}
        # total_counts = emoticon_counts.values()
        # emoticon_counts['total'] = total_counts

        for emoticon in emoticons:
            emoticon_counts[emoticon.emoticon_type] += 1

        comments_data = []
        for com in comments:
            comments_emoticons = Emoticon.objects.filter(related_comment=com)
            comments_emoticon_counts = {'like': 0, 'heart': 0, 'smile': 0, 'rage': 0}
            for emoticon in comments_emoticons:
                comments_emoticon_counts[emoticon.emoticon_type] += 1

            comment = {
                'id': com.id,
                'user_profile': {
                    'id': com.user_profile.id,
                    'first_name': com.user_profile.first_name,
                    'second_name': com.user_profile.last_name,
                    'profile_img': com.user_profile.profilepicture.image.url
                },
                'content': com.content,
                'created_at': com.created_at,
                'emoticon_counts': comments_emoticon_counts,
                'total_emoticon_count': sum(comments_emoticon_counts.values())
            }
            comments_data.append(comment)

        response_data = {
            'comments': comments_data,
            'emoticon_counts': emoticon_counts,
        }
        return JsonResponse(response_data)


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        to_user_profile = get_object_or_404(UserProfile, user__id=user_id)
        from_user_profile = request.user.userprofile
        if not FriendRequest.objects.filter(from_user=from_user_profile,
                                            to_user=to_user_profile).exists() and not from_user_profile.friends.filter(
            id=to_user_profile.id).exists():
            from_user_profile.send_friend_request(to_user_profile)
        return redirect('profile_dashboard')


class FriendRequestsView(LoginRequiredMixin, View):
    def get(self, request):
        received_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile, status='pending')
        friend_requests_data = [
            {
                'id': req.id,
                'from_user': {
                    'first_name': req.from_user.first_name,
                    'last_name': req.from_user.last_name,
                    'profile_picture': req.from_user.profilepicture.image.url
                }
            } for req in received_friend_requests
        ]
        return JsonResponse({
            'friend_requests_count': received_friend_requests.count(),
            'friend_requests': friend_requests_data
        })


class RejectFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)
        friend_request.reject()
        return redirect('profile_dashboard')


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)
        friend_request.accept()
        return redirect('profile_dashboard')


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return self.request.user.userprofile.friends.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        context['friends_queryset'] = self.get_queryset()
        return context

class GetReactionsView(View):
    def get(self, request, *args, **kwargs):
        item_type = request.GET.get('type')
        item_id = request.GET.get('id')

        if item_type == 'post':
            reactions = Emoticon.objects.filter(post_id=item_id).select_related('related_user')
        elif item_type == 'comment':
            reactions = Emoticon.objects.filter(related_comment_id=item_id).select_related('related_user')
        elif item_type == 'image':
            reactions = Emoticon.objects.filter(related_user_img_id=item_id).select_related('related_user')
        else:
            return JsonResponse({'success': False, 'error': 'Invalid type'})

        reactions_data = [{'user_first_name': reaction.related_user.first_name,
                           'type': reaction.emoticon_type,
                           'user_second_name': reaction.related_user.last_name,
                           'user_profile_img': reaction.related_user.profilepicture.image.url}
                          for reaction in reactions]

        return JsonResponse({'success': True, 'reactions': reactions_data})

class AddPostEmoticonView(View):
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        reactions = Emoticon.objects.filter(post_id=post_id).select_related('related_user')

        reactions_data = [{'user_first_name': reaction.related_user.first_name, 'type': reaction.emoticon_type,
                           'user_second_name': reaction.related_user.last_name,
                           'user_profile_img': reaction.related_user.profilepicture.image.url
                           } for reaction in reactions]

        return JsonResponse({'success': True, 'reactions': reactions_data})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        post_id = data.get('post_id')
        emoticon_type = data.get('emoticon_type')
        user_id = data.get('user_id')
        existing_emoticon = Emoticon.objects.filter(post_id=post_id, related_user_id=user_id).first()

        if existing_emoticon:
            if existing_emoticon.emoticon_type == emoticon_type:
                existing_emoticon.delete()
            else:
                existing_emoticon.emoticon_type = emoticon_type
                existing_emoticon.save()
        else:
            Emoticon.objects.create(emoticon_type=emoticon_type, related_user_id=user_id,
                                    post_id=post_id)

        return JsonResponse({'success': True})

class MakeProfilePictureView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        image_id = data.get('image_id')
        print(image_id)


        if not image_id:
            return JsonResponse({'success': False, 'error': 'Missing image_id'})

        try:

            image = get_object_or_404(UserImage, id=image_id)
            ProfilePicture.objects.filter(user_profile_id=request.user.id).update(image=image.image)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})