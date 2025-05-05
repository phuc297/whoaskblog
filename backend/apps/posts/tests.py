from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.posts.models import Post, Category, Comment, PostVote
import json
from faker import Faker
from random import choice, randrange
from utils.fake import FakeUtils


class PostsAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.raw_password = 'pass1234'
        self.user = User.objects.create_user(
            username=self.username, password=self.raw_password)
        self.profile = Profile.objects.get(user=self.user)
        self.fake = Faker()

        self.category = Category.objects.create(
            name="Test Category", description="A test category")

        data_post = {
            "author": self.profile,
            "title": self.fake.sentence(5),
            "content": "temp_string",
            "description": self.fake.sentence(5),
            "category": self.category
        }
        self.post = Post(author=data_post["author"], title=data_post["title"],
                         content=data_post["content"], category=data_post["category"], description=data_post["description"])

        self.post.content.json_string = FakeUtils.get_fake_content_quill()
        self.post.save()

    def test_post_view_returns_200_and_correct_template(self):
        response = self.client.get(
            reverse('posts:view', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post.html')

    def test_post_create_view_returns_200_and_correct_template(self):
        response = self.client.get(reverse('posts:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_create_post_successfully(self):
        logged_in = self.client.login(
            username=self.user.username, password=self.raw_password)
        self.assertTrue(logged_in)
        data = {
            'title': 'Test Title',
            'content': FakeUtils.get_fake_content_quill(),
            'description': self.fake.sentence(5),
            'category': self.category.id,
            'thumbnail': ''
        }
        response = self.client.post(reverse('posts:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Test Title').exists())

    def test_comment_redirects_to_login_if_not_authenticated(self):
        data = {
            'content': self.fake.sentence(5),
            'post_id': self.post.id
        }

        url = reverse('posts:comment', kwargs={'post_id': self.post.id})
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/users/login/?next={url}')

    def test_comment_successfully(self):
        logged_in = self.client.login(
            username=self.user.username, password=self.raw_password)
        self.assertTrue(logged_in)

        data = {
            'post_id': self.post.id,
            'content': self.fake.sentence(1)
        }

        url = reverse('posts:comment', kwargs={'post_id': self.post.id})
        response = self.client.post(url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_vote_redirects_to_login_if_not_authenticated(self):
        data = {
            'vote_choice': choice([-1, 1]),
        }

        url = reverse('posts:vote', kwargs={'post_id': self.post.id})
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/users/login/?next={url}')

    def test_post_vote_successfully(self):
        logged_in = self.client.login(
            username=self.user.username, password=self.raw_password)
        self.assertTrue(logged_in)

        old_vote_value = self.post.votes

        data = {
            'vote': choice([-1, 1]),
        }

        url = reverse('posts:vote', kwargs={'post_id': self.post.id})
        response = self.client.post(url, json.dumps(
            data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
