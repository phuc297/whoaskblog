import os
import random
from random import choice, randrange

from django.contrib.auth.models import User
from faker import Faker

from posts.models import Category, Post, Comment
from users.models import Profile

fake = Faker()


class Mock:
    def __init__(self, delete=False):
        if delete:
            self.delete_data()
        self.generate_users()
        self.create_follower()
        self.generate_categories()
        self.generate_posts()
        self.generate_comments()

    def delete_data(self):
        User.objects.all().filter(is_superuser=False).delete()
        Category.objects.all().delete()

    def generate_users(self):

        for i in range(0, 30):
            mock_user = {
                "username": fake.unique.user_name(),
                "password": "1",
                "email": fake.unique.email(),
                "bio": fake.text(max_nb_chars=80),
                "avatar": f"default_avatars/{random.choice(os.listdir("./mediafiles/"))}"
            }
            user = User.objects.create_user(username=mock_user["username"], password=mock_user["password"],
                                            email=mock_user["email"])
            user.save()
            profile = Profile.objects.create(
                user=user, bio=mock_user["bio"], avatar=mock_user["avatar"])
            profile.set_default_avatar()
            profile.save()

    def create_follower(self):
        all_profiles = Profile.objects.all()
        for profile in all_profiles:
            random_number = randrange(3, 10)
            random_follower = Profile.objects.order_by('?')[:random_number]
            for follower in random_follower:
                profile.followers.add(follower)

    def generate_posts(self):
        n_posts = 20
        categories = Category.objects.all()
        users = User.objects.all().filter(is_superuser=False)
        for i in range(0, n_posts):
            mock_post = {
                "author": choice(users),
                "title": fake.sentence(randrange(8, 10)),
                "content": fake.paragraph(200),
                "category": choice(categories)
            }
            post = Post(author=mock_post["author"], title=mock_post["title"],
                        content=mock_post["content"], category=mock_post["category"])
            post.save()

    def generate_comments(self):
        n_comments = 50
        posts = Post.objects.all()
        users = User.objects.all().filter(is_superuser=False)
        for i in range(0, n_comments):
            mock_comment = {
                "post": choice(posts),
                "user": choice(users),
                "content": fake.sentence(randrange(10, 80))
            }
            comment = Comment(
                post=mock_comment["post"], user=mock_comment["user"], content=mock_comment["content"])
            comment.save()

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
