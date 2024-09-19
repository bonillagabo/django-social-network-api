from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment


class PostTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="password123",
            email="user1@gmail.com",
            first_name="usuario1",
            last_name="example",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="password123",
            email="user2@gmail.com",
            first_name="usuario2",
            last_name="example",
        )

        self.post1 = Post.objects.create(author=self.user1, content="Post 1 by user1")
        self.post2 = Post.objects.create(author=self.user2, content="Post 2 by user2")

        self.comment1 = Comment.objects.create(
            author=self.user2, post=self.post1, content="Comment 1 on post 1"
        )
        self.comment2 = Comment.objects.create(
            author=self.user1, post=self.post1, content="Comment 2 on post 1"
        )
        self.comment3 = Comment.objects.create(
            author=self.user2, post=self.post1, content="Comment 3 on post 1"
        )
        self.comment4 = Comment.objects.create(
            author=self.user1, post=self.post1, content="Comment 4 on post 1"
        )

        self.token_url = reverse("token_obtain_pair")
        self.posts_url = reverse("posts")
        self.post_detail_url = lambda post_id: reverse("post_detail", args=[post_id])

        response = self.client.post(
            self.token_url, {"username": "user1", "password": "password123"}
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_posts(self):
        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][1]["content"], "Post 1 by user1")
        self.assertEqual(response.data["results"][0]["content"], "Post 2 by user2")

    def test_get_posts_filtered_by_author(self):
        response = self.client.get(self.posts_url, {"author_id": self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["content"], "Post 1 by user1")

    def test_create_post(self):
        data = {"author": self.user1.id, "content": "New post by user1"}
        response = self.client.post(self.posts_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New post by user1")
        self.assertEqual(Post.objects.count(), 3)

    def test_create_post_invalid_author(self):
        data = {
            "author": 9999,
            "content": "Post with invalid author",
        }
        response = self.client.post(self.posts_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("author", response.data)

    def test_get_post_detail(self):
        response = self.client.get(self.post_detail_url(self.post1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Post 1 by user1")
        self.assertEqual(response.data["author_username"], self.user1.username)
        comments = response.data["comments"]
        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0]["content"], "Comment 4 on post 1")
        self.assertEqual(comments[1]["content"], "Comment 3 on post 1")
        self.assertEqual(comments[2]["content"], "Comment 2 on post 1")

    def test_get_post_detail_no_comments(self):
        post_without_comments = Post.objects.create(
            author=self.user1, content="Post without comments"
        )
        response = self.client.get(self.post_detail_url(post_without_comments.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Post without comments")
        self.assertEqual(response.data["author_username"], self.user1.username)
        self.assertEqual(response.data["comments"], [])
        post_without_comments.delete()
