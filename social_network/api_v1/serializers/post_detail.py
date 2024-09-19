from rest_framework import serializers
from ..models.post import Post
from .user_detail import UserDetailSerializer
from .comment import CommentSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "content",
            "created_at",
            "comments",
        ]

    def get_comments(self, instance):
        return CommentSerializer(instance.limited_comments, many=True).data
