from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.users.models import Profile
import json


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Tạo 2 user và profile để test follow
        self.user1 = User.objects.create_user(
            username="user1", password="pass1234")
        self.user2 = User.objects.create_user(
            username="user2", password="pass1234")
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_logout_view(self):
        self.client.login(username="user1", password="pass1234")
        response = self.client.post(reverse("logout"))  # POST logout request
        # Check redirection to home
        self.assertRedirects(response, reverse("home"))

    def test_profile_view(self):
        url = reverse("profile", kwargs={"pk": self.profile1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        # Check the correct profile is rendered
        self.assertEqual(response.context["profile"], self.profile1)

    def test_follow_profile_follow(self):
        url = reverse("follow", kwargs={"profile_id": self.profile2.pk})
        payload = {
            "user_profile_id": self.profile1.pk,
            "profile_id": self.profile2.pk
        }
        response = self.client.post(url, data=json.dumps(
            payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.profile2.followers.filter(
            pk=self.profile1.pk).exists())  # Check if follow is successful
        self.assertJSONEqual(response.content, {
            "success": True,
            "user_id": self.profile1.pk,
            "profile_id": self.profile2.pk,
            "msg": "follow success"
        })

    def test_follow_profile_unfollow(self):
        self.profile2.followers.add(self.profile1)  # Add follower initially
        url = reverse("follow", kwargs={"profile_id": self.profile2.pk})
        payload = {
            "user_profile_id": self.profile1.pk,
            "profile_id": self.profile2.pk
        }
        response = self.client.post(url, data=json.dumps(
            payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.profile2.followers.filter(
            pk=self.profile1.pk).exists())  # Check if unfollow is successful
        self.assertJSONEqual(response.content, {
            "success": True,
            "user_id": self.profile1.pk,
            "profile_id": self.profile2.pk,
            "msg": "unfollow success"
        })
