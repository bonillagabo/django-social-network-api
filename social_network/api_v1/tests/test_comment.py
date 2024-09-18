from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models.user import User
from ..models.comment import Comment
from ..models.post import Post


class CommentTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="password123",
            email="user1@gmail.com",
            name="usuario1",
            lastname="example",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="password123",
            email="user2@gmail.com",
            name="usuario2",
            lastname="example",
        )

        self.post = Post.objects.create(author=self.user1, content="This is a post")

        self.comment1 = Comment.objects.create(
            author=self.user2, post=self.post, content="This is a comment"
        )

        self.token_url = reverse("token_obtain_pair")
        self.comments_url = lambda post_id: reverse("comments", args=[post_id])

        response = self.client.post(
            self.token_url, {"username": "user1", "password": "password123"}
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_comments(self):
        response = self.client.get(self.comments_url(self.post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "This is a comment")
        self.assertEqual(response.data[0]["author"], self.user2.id)
        self.assertEqual(response.data[0]["post"], self.post.id)

    def test_create_comment(self):
        data = {
            "author": self.user1.id,
            "post": self.post.id,
            "content": "Another comment",
        }
        response = self.client.post(
            self.comments_url(self.post.id), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Another comment")
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment_invalid(self):
        data = {
            "content": "",
        }
        response = self.client.post(
            self.comments_url(self.post.id), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)
