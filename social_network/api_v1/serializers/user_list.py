from rest_framework import serializers
from ..models.user import User


class UserListSerializer(serializers.ModelSerializer):
    """Serializer para listar usuarios con campos mínimos"""

    class Meta:
        model = User
        fields = ["id", "username"]
