from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import BlogPost, BlogCategory
from .forms import BlogPostForm


def blog_list_view(request):
    category_slug = request.GET.get('category')
    posts = BlogPost.objects.filter(status='published')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    categories = BlogCategory.objects.all()
    return render(request, 'blog/blog_list.html', {
        'posts': posts, 'categories': categories, 'selected_category': category_slug
    })


def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    return render(request, 'blog/blog_detail.html', {'post': post})


@login_required
def my_posts_view(request):
    if request.user.user_type != 'doctor':
        raise PermissionDenied("Only doctors can manage posts.")
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def blog_create_view(request):
    if request.user.user_type != 'doctor':
        raise PermissionDenied("Only doctors can create posts.")
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('blog:my_posts')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Create'})


@login_required
def blog_update_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.author != request.user:
        raise PermissionDenied("You can only edit your own posts.")
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('blog:my_posts')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Update', 'post': post})


@login_required
def blog_delete_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.author != request.user:
        raise PermissionDenied("You can only delete your own posts.")
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('blog:my_posts')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})
