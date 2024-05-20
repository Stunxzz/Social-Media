from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from Profiles.forms import ProfileCreationForm, EmailAuthenticationForm, UserProfileForm, PostCreationForm, \
    CommentCreationForm
from Profiles.models import Profile, UserProfile, Post, Comment, ProfilePicture


class CreateProfileView(CreateView):
    model = Profile
    form_class = ProfileCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy("profile_info")

    def form_valid(self, form):
        form.save()
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = EmailAuthenticationForm

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        if hasattr(self.user, 'userprofile'):
            return redirect('profile_dashboard')
        else:
            return redirect('profile_info')


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'create_user_profile.html'

    def form_valid(self, form):
        user_profile = form.save(commit=False)
        user_profile.user = self.request.user
        user_profile.save()

        profile_picture = form.cleaned_data.get('profile_picture')
        if profile_picture:
            ProfilePicture.objects.update_or_create(user_profile=user_profile, defaults={'image': profile_picture})
        else:
            ProfilePicture.objects.update_or_create(user_profile=user_profile,
                                                    defaults={'image': 'profile_pictures/blank-profil.webp'})

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_dashboard')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profiles = UserProfile.objects.exclude(user=self.request.user)
        posts = Post.objects.all()
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