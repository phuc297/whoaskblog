# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from apps.users.models import Profile
# from apps.posts.models import Post, Category, Comment, PostVote
# import json


# class PostViewsTestCase(TestCase):
#     def setUp(self):
#         # Create user and profile
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username="testuser", password="password123")
#         self.profile = Profile.objects.create(user=self.user)

#         # Create a category
#         self.category = Category.objects.create(
#             name="Test Category", description="A test category")

#         # Create a post
#         self.post = Post.objects.create(
#             author=self.profile,
#             title="Test Post",
#             content="Test content",
#             description="Test description",
#             category=self.category
#         )

#     def test_create_post_view_get(self):
#         # Test the GET request for the create post view
#         response = self.client.get(reverse("posts:create"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "posts/create_post.html")

#     def test_create_post_view_post(self):
#         # Test the POST request to create a new post
#         data = {
#             "title": "New Post",
#             "content": "This is the content of the new post.",
#             "description": "Description of the new post.",
#             "category": self.category.id
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:create"), data)
#         # Expecting a redirect after post creation
#         self.assertEqual(response.status_code, 302)
#         # Check if the post is created
#         self.assertTrue(Post.objects.filter(title="New Post").exists())

#     def test_post_view_get(self):
#         # Test the GET request for viewing a post
#         response = self.client.get(
#             reverse("posts:view", kwargs={"pk": self.post.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "posts/post.html")
#         self.assertEqual(response.context["post"], self.post)

#     def test_comment_post(self):
#         # Test the POST request for adding a comment
#         comment_data = {
#             "content": "This is a comment.",
#             "post_id": self.post.id
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:comment", kwargs={"post_id": self.post.pk}),
#                                     json.dumps(comment_data), content_type="application/json")
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             "success": True,
#             "username": self.profile.user.username,
#             "content": "This is a comment.",
#             "avatar": self.profile.avatar.url,
#             "created_at": response.json()['created_at']
#         })

#         # Check if comment is saved
#         self.assertTrue(Comment.objects.filter(
#             content="This is a comment.").exists())

#     def test_post_vote_upvote(self):
#         # Test the POST request for voting (upvote)
#         vote_data = {
#             "vote": PostVote.UPVOTE
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:vote", kwargs={"post_id": self.post.pk}),
#                                     json.dumps(vote_data), content_type="application/json")
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             "success": True,
#             "message": "Vote added",
#             "votes": 1,  # The total votes for this post
#             "vote_choice": 1  # The vote choice (upvote)
#         })
#         # Ensure one vote is recorded
#         self.assertEqual(self.post.post_votes.count(), 1)

#     def test_post_vote_downvote(self):
#         # Test the POST request for voting (downvote)
#         vote_data = {
#             "vote": PostVote.DOWNVOTE
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:vote", kwargs={"post_id": self.post.pk}),
#                                     json.dumps(vote_data), content_type="application/json")
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             "success": True,
#             "message": "Vote added",
#             "votes": -1,  # The total votes for this post (downvoted)
#             "vote_choice": -1  # The vote choice (downvote)
#         })
#         # Ensure one vote is recorded
#         self.assertEqual(self.post.post_votes.count(), 1)

#     def test_invalid_comment(self):
#         # Test invalid comment (empty content)
#         comment_data = {
#             "content": "",
#             "post_id": self.post.id
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:comment", kwargs={"post_id": self.post.pk}),
#                                     json.dumps(comment_data), content_type="application/json")
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             "success": False,
#             "error": "Empty Comment"
#         })

#     def test_invalid_vote(self):
#         # Test invalid vote value (not 1 or -1)
#         vote_data = {
#             "vote": 0  # Invalid vote
#         }
#         self.client.login(username="testuser", password="password123")
#         response = self.client.post(reverse("posts:vote", kwargs={"post_id": self.post.pk}),
#                                     json.dumps(vote_data), content_type="application/json")
#         self.assertEqual(response.status_code, 400)
#         self.assertJSONEqual(response.content, {
#             "success": False,
#             "error": "Invalid vote value."
#         })
