from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.users.models import Profile
import json


class UserAppsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.raw_password = 'pass1234'
        self.user1 = User.objects.create_user(
            username='user1', password=self.raw_password)
        self.user2 = User.objects.create_user(
            username='user2', password=self.raw_password)
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

    # User Test Case

    def test_signup_view_returns_200_and_correct_template(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_creates_user_and_redirects(self):
        data = {
            'username': 'newuser',
            'email': 'user_email@email.com',
            'password': 'mypassword123',
            'confirm_password': 'mypassword123',
        }
        response = self.client.post(reverse('users:signup'), data)
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username=data['username'])
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, data['username'])
        self.assertRedirects(response, reverse('home'))

    def test_login_view_returns_200_and_correct_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_redirects_to_home_on_success(self):
        data = {
            'username': 'user1',
            'password': self.raw_password,
        }
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    # Profile Test Case

    def test_profile_view_returns_200_and_correct_template_and_correct_context(self):
        response = self.client.get(
            reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['profile'], self.profile1)

    def test_follow_profile_redirects_to_login_if_not_authenticated(self):
        data = {
            'profile_id': self.user2.id
        }
        response = self.client.post(
            reverse('users:follow', kwargs={'profile_id': self.profile2.id}), data)
        self.assertRedirects(
            response, f'/users/login/?next=/users/{data['profile_id']}/follow')

    def test_follow_profile_successfully(self):
        logged_in = self.client.login(
            username=self.user1.username, password=self.raw_password)
        self.assertTrue(logged_in)

        data = {
            'profile_id': self.user2.id
        }
        response = self.client.post(
            reverse('users:follow', kwargs={'profile_id': self.profile2.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {
            'success': True,
            'user_id': self.profile1.id,
            'profile_id': self.profile2.id,
            'msg': 'follow success'
        })
        self.assertIn(self.profile1, self.profile2.followers.all())

    def test_unfollow_profile_successfully(self):
        self.profile2.followers.add(self.profile1)

        logged_in = self.client.login(
            username=self.user1.username, password=self.raw_password)
        self.assertTrue(logged_in)

        data = {
            'profile_id': self.user2.id
        }
        response = self.client.post(
            reverse('users:follow', kwargs={'profile_id': self.profile2.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {
            'success': True,
            'user_id': self.profile1.id,
            'profile_id': self.profile2.id,
            'msg': 'unfollow success'
        })
        self.assertNotIn(self.profile1, self.profile2.followers.all())
