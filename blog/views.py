from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.forms import CommentForm
from blog.models import Post, Comment


def blog_index(request):
    posts = Post.objects.all().order_by("-created_at")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        category__name__contains=category
    ).order_by("-created_at")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=request.user,
                content=form.data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post, is_active=True)
    media_files = post.media.all()

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        'media_files': media_files
    }
    return render(request, "blog/detail.html", context)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is not None and password is not None:
        user = User.objects.create_user(username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Username and password are required'})

