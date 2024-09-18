from django.urls import path
from ..views.post import posts, comments, post_detail

urlpatterns = [
    path("posts/", posts, name="posts"),
    path("posts/<int:post_id>/comments/", comments, name="comments"),
    path("posts/<int:post_id>/", post_detail, name="post_detail"),
]
