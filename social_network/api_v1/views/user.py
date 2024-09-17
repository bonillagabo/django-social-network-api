from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.user import User
from ..serializers.user_detail import UserDetailSerializer
from ..serializers.user_list import UserListSerializer


@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
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
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
def follow_user(request, user_id, follow_id):
    try:
        user = User.objects.get(pk=user_id)
        follow_user = User.objects.get(pk=follow_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if follow_user in user.following.all():
        return Response(
            {"message": "Already following this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.following.add(follow_user)
    user.save()

    return Response({"message": "Now following user."}, status=status.HTTP_200_OK)
