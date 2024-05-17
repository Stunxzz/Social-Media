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
        posts = self.get_queryset()
        comments = Comment.objects.filter(post__in=posts)
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profiles = UserProfile.objects.all()
        context['user_profiles'] = user_profiles
        context['user_profile'] = user_profile
        context['comments'] = comments
        context['post_form'] = PostCreationForm()
        context['comment_form'] = CommentCreationForm()
        return context