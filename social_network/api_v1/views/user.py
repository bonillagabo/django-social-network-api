from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utils.custom_paginator import CustomPageNumberPagination
from ..models.user import User
from ..serializers.user_detail import UserDetailSerializer
from ..serializers.user_list import UserListSerializer
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        paginator = CustomPageNumberPagination()
        users = User.objects.all()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserListSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = (
            User.objects.select_related()
            .prefetch_related("following", "followers")
            .get(pk=pk)
        )
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
def follow_user(request, user_id, follow_id):
    user = get_object_or_404(User, pk=user_id)
    follow_user = get_object_or_404(User, pk=follow_id)

    if user.following.filter(pk=follow_user.pk).exists():
        return Response(
            {"message": "Already following this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.following.add(follow_user)
    return Response({"message": "Now following user."}, status=status.HTTP_200_OK)
