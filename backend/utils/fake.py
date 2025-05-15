import json
import os
import random
from random import choice, randrange
import sys

from django.contrib.auth.models import User
from faker import Faker

from apps.posts.models import Category, Post, Comment
from apps.users.models import Profile
from apps.notifications.models import Notification
from apps.chat.models import Conversation
from apps.core.signals import disable_signal
from utils.utils import get_random_avatar, get_random_thumbnail
from django.db.models.signals import post_save, m2m_changed
from apps.users.signals import create_profile_on_new_user
fake = Faker()


class FakeUtils:

    @staticmethod
    def get_fake_content_quill(paragraph=5):
        content_text = fake.paragraph(paragraph)
        content_quill = {
            "delta": {
                "ops": [
                     {"insert": content_text + "\n"}
                ]
            },
            "html": f"<p>{content_text}</p>"
        }
        return json.dumps(content_quill)


class Fake:
    def __init__(self, generate=False, delete=False):
        if delete:
            self.delete_data()
        if generate:
            self.generate_users(50)
            self.create_follower(2, 10)
            self.generate_categories()
            self.generate_posts(40)
            self.generate_comments(100)

    def delete_data(self):
        User.objects.all().filter(is_superuser=False).delete()
        Category.objects.all().delete()
        Notification.objects.all().delete()
        Conversation.objects.all().delete()

    def generate_users(self, number):
        users = []
        profiles = []
        with disable_signal(post_save, create_profile_on_new_user, User):
            for _ in range(number):
                mock_user = {
                    "username": fake.unique.user_name(),
                    "password": "1",
                    "email": fake.unique.email(),
                    "bio": fake.text(max_nb_chars=80)
                }
                user = User.objects.create_user(username=mock_user["username"], password=mock_user["password"],
                                                email=mock_user["email"])
                sys.stdout.write("create a user successful !\n")
                sys.stdout.flush()
                profile = Profile(
                    user=user, bio=mock_user["bio"], display_name=mock_user["username"])
                profiles.append(profile)
            Profile.objects.bulk_create(profiles)
            sys.stdout.write(f"create {len(profiles)} profiles successful !\n")
            sys.stdout.flush()

    def create_follower(self, min, max):
        all_profiles = Profile.objects.all()
        for profile in all_profiles:
            random_number = randrange(min, max)
            random_follower = Profile.objects.order_by('?')[:random_number]
            for follower in random_follower:
                profile.followers.add(follower)

    def generate_posts(self, n_posts):
        posts = []
        categories = Category.objects.all()
        profiles = Profile.objects.all()
        for i in range(0, n_posts):
            mock_post = {
                "author": choice(profiles),
                "title": fake.sentence(randrange(8, 10)),
                "content": "temp_string",
                "description": fake.sentence(randrange(8, 10)),
                "category": choice(categories)
            }
            post = Post(author=mock_post["author"], title=mock_post["title"],
                        content=mock_post["content"], category=mock_post["category"], description=mock_post["description"])
            content_text = fake.paragraph(200)
            content_quill = {
                "delta": {
                    "ops": [
                        {"insert": content_text + "\n"}
                    ]
                },
                "html": f"<p>{content_text}</p>"
            }
            post.content.json_string = json.dumps(content_quill)
            post.status = Post.PUBLISHED
            posts.append(post)
        Post.objects.bulk_create(posts)
        sys.stdout.write(f"create {len(posts)} posts successful !\n")
        sys.stdout.flush()

    def generate_comments(self, n_comments):
        comments = []
        posts = Post.objects.all()
        commenter = Profile.objects.all()
        for i in range(0, n_comments):
            mock_comment = {
                "post": choice(posts),
                "commenter": choice(commenter),
                "content": fake.sentence(randrange(10, 80))
            }
            comment = Comment(
                post=mock_comment["post"], commenter=mock_comment["commenter"], content=mock_comment["content"])
            comments.append(comment)
        Comment.objects.bulk_create(comments)
        sys.stdout.write(f"create {len(comments)} comments successful !\n")
        sys.stdout.flush()

    def generate_categories(self):
        # categories = [
        #     {"name": "Công nghệ",
        #         "description": "Các bài viết về phần mềm, AI, lập trình, IoT."},
        #     {"name": "Kinh tế", "description": "Chia sẻ về tài chính, đầu tư, kinh doanh."},
        #     {"name": "Đời sống", "description": "Những câu chuyện về cuộc sống, xã hội."},
        #     {"name": "Khoa học",
        #         "description": "Vật lý, hóa học, sinh học, khám phá vũ trụ."},
        #     {"name": "Sách",  "description": "Review sách, thảo luận, chia sẻ tài liệu."},
        #     {"name": "Phim ảnh",
        #         "description": "Review phim, series Netflix, bàn luận điện ảnh."},
        #     {"name": "Âm nhạc", "description": "Nhạc Việt, nhạc Âu Mỹ, K-pop, indie."},
        #     {"name": "Game",  "description": "Esports, game PC, console, mobile."},
        #     {"name": "Thể thao", "description": "Bóng đá, bóng rổ, chạy bộ, gym."},
        #     {"name": "Lịch sử",
        #         "description": "Kiến thức lịch sử, chiến tranh, nhân vật lịch sử."},
        #     {"name": "Du lịch", "description": "Kinh nghiệm du lịch, review địa điểm."},
        #     {"name": "Ẩm thực", "description": "Nấu ăn, review quán ăn, món ngon."},
        #     {"name": "Tâm lý học", "description": "Phát triển bản thân, tâm lý xã hội."},
        #     {"name": "Lập trình", "description": "Python, JavaScript, Web development."},
        #     {"name": "Thiết kế", "description": "UI/UX, đồ họa, branding, Photoshop."},
        #     {"name": "Nghệ thuật",
        #         "description": "Hội họa, điêu khắc, sáng tạo nghệ thuật."},
        #     {"name": "Khởi nghiệp",
        #         "description": "Kinh nghiệm startup, gọi vốn, phát triển dự án."},
        #     {"name": "Học tập",
        #         "description": "Kinh nghiệm học tập, ngoại ngữ, mẹo học nhanh."},
        #     {"name": "Công việc",
        #         "description": "Nghề nghiệp, tuyển dụng, kinh nghiệm làm việc."},
        #     {"name": "Truyện ngắn", "description": "Sáng tác, truyện ngắn, tiểu thuyết."},
        # ]

        categories = [
            {
                "name": "Thời sự",
                "description": "Cập nhật tin tức thời sự trong nước và quốc tế, các vấn đề chính trị, xã hội, kinh tế nóng hổi."
            },
            {
                "name": "Thể thao",
                "description": "Tin tức thể thao mới nhất, bình luận, kết quả các trận đấu, giải đấu trong nước và quốc tế."
            },
            {
                "name": "Giải trí",
                "description": "Tin tức giải trí, điện ảnh, âm nhạc, đời sống nghệ sĩ, các sự kiện văn hóa nghệ thuật."
            },
            {
                "name": "Kinh doanh",
                "description": "Tin tức kinh tế, tài chính, chứng khoán, doanh nghiệp, thị trường và các xu hướng kinh doanh mới nhất."
            },
            {
                "name": "Pháp luật",
                "description": "Tin tức pháp luật, các vụ án nổi bật, tư vấn pháp lý và các thông tin liên quan đến an ninh trật tự."
            },
        ]

        for cat in categories:
            c = Category.objects.get_or_create(
                name=cat["name"], description=cat["description"])
