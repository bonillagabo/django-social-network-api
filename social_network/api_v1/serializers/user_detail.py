from rest_framework import serializers
from ..models.user import User
from ..serializers.user_list import UserListSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para mostrar el detalle completo de un usuario"""

    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    posts_count = serializers.IntegerField(source="posts.count", read_only=True)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "lastname",
            "password",
            "comments_count",
            "posts_count",
            "followers_count",
            "following_count",
            "following",
            "followers",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)
        return representation

    def get_following(self, obj):
        return UserListSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return UserListSerializer(obj.followers.all(), many=True).data
