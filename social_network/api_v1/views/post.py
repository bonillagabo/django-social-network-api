from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..serializers.post import PostSerializer
from ..serializers.post_detail import PostDetailSerializer
from ..serializers.comment import CommentSerializer
from ..serializers.user_detail import UserDetailSerializer
from ..utils.custom_paginator import CustomPageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from datetime import datetime, timedelta


@api_view(["GET", "POST"])
def posts(request):
    if request.method == "GET":
        author_id = request.query_params.get("author_id")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        posts = Post.objects.all()

        if author_id:
            posts = posts.filter(author_id=author_id)
        if from_date:
            posts = posts.filter(created_at__gte=from_date)
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            posts = posts.filter(created_at__lte=to_date)

        paginator = CustomPageNumberPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=request.data["author"])
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
def comments(request, post_id):
    if request.method == "GET":
        post = get_object_or_404(
            Post.objects.prefetch_related("comments__author"), pk=post_id
        )
        comments = post.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        request.data["post"] = post_id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            post = get_object_or_404(Post, pk=post_id)
            serializer.save(author=post.author, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.select_related("author").order_by(
                    "-created_at"
                )[:3],
                to_attr="limited_comments",
            )
        ),
        pk=post_id,
    )
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)
