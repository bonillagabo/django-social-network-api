from django.urls import include, path

urlpatterns = [
    path("", include("api_v1.urls.user")),
]
