from django.urls import path
from ..views.user import users_endpoint_handler, user_detail, follow_user

urlpatterns = [
    path("users/", users_endpoint_handler, name="user_endpoint_handler"),
    path("users/<int:user_id>/", user_detail, name="user_detail"),
    path(
        "users/<int:user_id>/follow/<int:follow_id>/", follow_user, name="follow_user"
    ),
]
