from posts.models import Post, Comment, Album, UserImage
from django import forms

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'content': 'What do you think?',
        }


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a comment ...'}),
        }
        labels = {
            'content': ''
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['album', 'image']