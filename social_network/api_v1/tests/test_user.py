from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models.user import User


class UserTests(APITestCase):
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

        self.token_url = reverse("token_obtain_pair")
        self.user_endpoint_handler_url = reverse("user_endpoint_handler")
        self.user_detail_url = lambda user_id: reverse("user_detail", args=[user_id])
        self.follow_user_url = lambda user_id, follow_id: reverse(
            "follow_user", args=[user_id, follow_id]
        )

        response = self.client.post(
            self.token_url, {"username": "user1", "password": "password123"}
        )

        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_user_list(self):
        response = self.client.get(self.user_endpoint_handler_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["username"], self.user1.username)
        self.assertEqual(response.data["results"][1]["username"], self.user2.username)

    def test_create_user(self):
        data = {
            "username": "user3",
            "password": "password123",
            "email": "user3@gmail.com",
            "name": "usuario3",
            "lastname": "example",
        }
        response = self.client.post(self.user_endpoint_handler_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully")
        user = User.objects.get(username="user3")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "user3@gmail.com")

    def test_get_user_detail(self):
        response = self.client.get(self.user_detail_url(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user1.username)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["name"], self.user1.name)
        self.assertEqual(response.data["lastname"], self.user1.lastname)

    def test_get_user_detail_not_found(self):
        response = self.client.get(self.user_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_user(self):
        response = self.client.post(self.follow_user_url(self.user1.id, self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Now following user.")
        self.user1.refresh_from_db()
        self.assertIn(self.user2, self.user1.following.all())

    def test_follow_user_already_following(self):
        self.user1.following.add(self.user2)
        response = self.client.post(self.follow_user_url(self.user1.id, self.user2.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Already following this user.")
        self.user1.refresh_from_db()
        self.assertIn(self.user2, self.user1.following.all())
