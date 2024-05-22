from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from Profiles.models import UserProfile
from posts.forms import PostCreationForm, CommentCreationForm, AlbumForm, UserImageForm
from posts.models import Post, Comment, Album


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profiles = UserProfile.objects.exclude(user=self.request.user)
        posts = Post.objects.all().order_by('-created_at')
        comments = Comment.objects.filter(post__in=posts)

        context['posts'] = posts
        context['comments'] = comments
        context['user_profiles'] = user_profiles
        context['user_profile'] = user_profile
        context['post_form'] = PostCreationForm()
        context['comment_form'] = CommentCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        post_form = PostCreationForm(request.POST)
        comment_form = CommentCreationForm(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'post_form' and post_form.is_valid():
            print('POST')
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

        return self.get(request, *args, **kwargs)


class CreateAlbumView(View):
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
            return redirect('profile_dashboard')
        user_profile = request.user.userprofile
        albums = Album.objects.filter(user_profile=user_profile)
        return render(request, self.template_name, {'form': form, 'albums': albums})


class UploadImageView(View):
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