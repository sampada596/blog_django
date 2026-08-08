from django.shortcuts import render , get_object_or_404, redirect
from .models import Post, Comment, Category, Tag
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm 
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm , PostForm , CommentForm 
from django.db.models import Q

def home(request):
    from django.contrib.auth.models import User
    from .models import Comment, Tag
    posts = Post.objects.filter(status='published').order_by('-created_at')
    total_posts = posts.count()
    total_authors = User.objects.filter(post__status='published').distinct().count()
    total_comments = Comment.objects.count()
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:4]
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:4]
    all_tags = Tag.objects.all()
    categories = Category.objects.all()
    sidebar_categories = []
    for category in categories:
        count = Post.objects.filter(category=category, status='published').count()
        sidebar_categories.append({'category': category, 'count': count})
    return render(request, 'blog/home.html', {
        'posts': posts,
        'total_posts': total_posts,
        'total_authors': total_authors,
        'total_comments': total_comments,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'all_tags': all_tags,
        'sidebar_categories': sidebar_categories,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('home')
    post_pk = comment.post.pk
    comment.delete()
    post = get_object_or_404(Post, pk=post_pk)
    return redirect('post_detail', slug=post.slug)

def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    ).order_by('-created_at') if query else []
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', slug=post.slug)

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/dashboard.html', {
        'user_posts': user_posts,
        
    })

def categories_list(request):
    categories = Category.objects.all()
    category_data = []
    for category in categories:
        count = Post.objects.filter(category=category, status='published').count()
        category_data.append({'category': category, 'count': count})
    return render(request, 'blog/categories.html', {'category_data': category_data})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-created_at')
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

def author_profile(request, username):
    from django.contrib.auth.models import User
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='published').order_by('-created_at')
    return render(request, 'blog/author_profile.html', {
        'author': author,
        'posts': posts,
    })

def about(request):
    return render(request, 'blog/about.html')


    