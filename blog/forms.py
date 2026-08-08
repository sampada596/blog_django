from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Tag

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'featured_image', 'image_alt', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Enter post title'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['rows'] = 10
        self.fields['content'].widget.attrs['placeholder'] = 'Write your post here...'
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['category'].empty_label = 'Select a category (optional)'
        self.fields['tags'].widget.attrs['class'] = 'form-select'
        self.fields['featured_image'].widget.attrs['class'] = 'form-control'
        self.fields['image_alt'].widget.attrs['class'] = 'form-control'
        self.fields['image_alt'].widget.attrs['placeholder'] = 'Describe the image (optional)'
        self.fields['status'].widget.attrs['class'] = 'form-select'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'form-control'
            })
        }

