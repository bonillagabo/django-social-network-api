from rest_framework import serializers
from ..models.post import Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "author", "author_username", "content", "created_at"]
