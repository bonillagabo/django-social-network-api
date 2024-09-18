from rest_framework import serializers
from ..models.post import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "content", "created_at"]
