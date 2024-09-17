from django.urls import path
from ..views.user import user_list, user_detail, follow_user

urlpatterns = [
    path("users/", user_list, name="user_list"),
    path("users/<int:pk>/", user_detail, name="user_detail"),
    path(
        "users/<int:user_id>/follow/<int:follow_id>/", follow_user, name="follow_user"
    ),
]
