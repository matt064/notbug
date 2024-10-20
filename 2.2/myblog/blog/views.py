from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import BlogPost
from .forms import BlogPostForm


def main_site(request):
    "Main site of project"
    posts = BlogPost.objects.all()

    context = {'posts': posts}
    return render(request, 'blog/main_site.html', context)


def sing_up_page(request):
    "registration a new user"
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:main_site')
    else:
        form = UserCreationForm()
    
    context = {'form': form }

    return render(request, 'blog/register.html', context)


def logout_page(request):
    "logout a user"
    logout(request)
    return redirect('blog:main_site')
  

@login_required
def post_create(request):
    "create a new blog post"
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:main_site')
    else:
        form = BlogPostForm()
    
    context = {'form': form}

    return render(request, 'blog/blog_form.html', context)


@login_required
def post_update(request, pk):
    "edit post"
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('blog:main_site')
    
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:main_site')
    else:
        form = BlogPostForm(instance=post)
    
    context = {'form': form}

    return render(request, 'blog/blog_form.html', context)

