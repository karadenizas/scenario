from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm,\
                   CommentForm, PostForm, PostEditForm
from .models import Profile, Post, Comment, Like, CommentLike
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


def index(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 30)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'posts': posts
    }

    return render(request, 'story/index.html', context)


def most_liked(request):
    object_list = Post.published.annotate(like_count=Count('liked')).order_by('-like_count')
    paginator = Paginator(object_list, 11)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'posts': posts
    }

    return render(request, 'story/most_liked.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', 
                                        {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()

    context = {
        'user_form': user_form
    }

    return render(request, 'account/register.html', context)


@login_required
def account(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                    data=request.POST, files=request.FILES)
                
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Account updated successfully')
        else:
            messages.error(request, 'Error updating your account')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'account/account.html', context)


@login_required
def most_liked_comments(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

    comments = post.comments.filter(active=True)
    ml_comments = comments.annotate(like_count=Count('liked')).order_by('-like_count')
    page = request.GET.get('page')

    ml_paginator = Paginator(ml_comments, 3)

    try:
        ml_viewComments = ml_paginator.page(page)
    except PageNotAnInteger:
        ml_viewComments = ml_paginator.page(1)
    except EmptyPage:
        ml_viewComments = ml_paginator.page(ml_paginator.num_pages)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added')
            return redirect(post)

    user = request.user
    if request.method == 'POST':
        if request.POST.get('comment_id'):
            comment_id = request.POST.get('comment_id')
            comment_obj = Comment.objects.get(id=comment_id)

            if user in comment_obj.liked.all():
                comment_obj.liked.remove(user)
            else:
                comment_obj.liked.add(user)
            
            commentLike, created = CommentLike.objects.get_or_create(user=user, comment_id=comment_id)

            if not created:
                if commentLike.value == 'Like':
                    commentLike.value = 'Unlike'
                else:
                    commentLike.value = 'Like'
            commentLike.save()
            return HttpResponseRedirect('')
                    
            context = {
                'ml_viewComments': ml_viewComments,
                'page': page,
                'post': post,
                'comments': comments
            }

            return render(request, 'story/most_liked_comments.html', context)

    else:
        comment_form = CommentForm()

    context = {
        'ml_viewComments': ml_viewComments,
        'page': page,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'story/most_liked_comments.html', context)



@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    
    comments = post.comments.filter(active=True)
    ml_comments = comments.annotate(like_count=Count('liked')).order_by('-like_count')
    new_comment = None
    # paginator last comments
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    
    try:
        viewComments = paginator.page(page)
    except PageNotAnInteger:
        viewComments = paginator.page(1)
    except EmptyPage:
        viewComments = paginator.page(paginator.num_pages)
    
    #paginator most liked comments
    ml_paginator = Paginator(ml_comments, 3)

    try:
        ml_viewComments = ml_paginator.page(page)
    except PageNotAnInteger:
        ml_viewComments = ml_paginator.page(1)
    except EmptyPage:
        ml_viewComments = ml_paginator.page(ml_paginator.num_pages)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added')
            return redirect(post)
        
    user = request.user
    if request.method == 'POST':
        if request.POST.get('post_id'):
            post_id = request.POST.get('post_id')
            post_obj = Post.objects.get(id=post_id)

            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
            else:
                post_obj.liked.add(user)
            
            like, created = Like.objects.get_or_create(user=user, post_id=post_id)

            if not created:
                if like.value == 'Like':
                    like.value = 'Unlike'
                else:
                    like.value = 'Like'
            like.save()
            return redirect(post)

    if request.method == 'POST':
        if request.POST.get('comment_id'):
            comment_id = request.POST.get('comment_id')
            comment_obj = Comment.objects.get(id=comment_id)

            if user in comment_obj.liked.all():
                comment_obj.liked.remove(user)
            else:
                comment_obj.liked.add(user)
            
            commentLike, created = CommentLike.objects.get_or_create(user=user, comment_id=comment_id)

            if not created:
                if commentLike.value == 'Like':
                    commentLike.value = 'Unlike'
                else:
                    commentLike.value = 'Like'
            commentLike.save()
            return redirect(post)

    else:
        comment_form = CommentForm()
    

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'viewComments': viewComments,
        'page': page,
        'ml_viewComments': ml_viewComments,
    }

    return render(request, 'story/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            title = request.POST.get('title')
            new_post.slug = slugify(title)
            new_post.save()

            return redirect('index')

    else:
        post_form = PostForm()
    
    context = {
        'post_form': post_form
    }

    return render(request, 'story/create_post.html', context)


@login_required
def my_stories(request):
    user = request.user
    post = Post.published.filter(author=user.id)
    paginator = Paginator(post, 4)
    page = request.GET.get('page')

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'page': page,
    }

    return render(request, 'story/my_stories.html', context)


@login_required
def my_comments(request):
    user = request.user
    comments = Comment.objects.filter(author=user.id)
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'comments': comments,
        'page': page,
    }

    return render(request, 'story/my_comments.html', context)


@login_required
def drafted(request):
    post = Post.objects.filter(status='draft', author=request.user.id)

    context = {
        'post':post
    }

    return render(request, 'story/drafted.html', context)


@login_required
def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, 
                            status='draft',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    if post.author != request.user:
        return redirect('index')
        

    if request.method == 'POST':
        edited_body = request.POST.get('body')
        edited_title = request.POST.get('title')
        if Post.objects.filter(title__iexact=edited_title, status='published').exists():
            messages.error(request, 'This title is already exist! Please enter an another title or add a number at the end of the title')
            post_form = PostForm(instance=post)
        else:
            Post.objects.filter(id=post.id).update(title=edited_title, body=edited_body, status='published')
            return redirect('index')
    
    else:
        post_form = PostForm(instance=post)

    context = {
        'post': post,
        'post_form': post_form
    }

    return render(request, 'story/post_edit.html', context)


def test(request):
    return render(request, 'test.html')