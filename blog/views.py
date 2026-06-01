from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})
