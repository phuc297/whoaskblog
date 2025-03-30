import random
from django.contrib.auth.models import User
from apps.posts.models import Category, Post, Comment
from faker import Faker

# Khởi tạo Faker
fake = Faker()

# Tạo dữ liệu ngẫu nhiên cho Category
categories = []
for _ in range(5):
    category_name = fake.unique.word().capitalize()
    category_description = fake.text(max_nb_chars=100)
    category = Category.objects.create(name=category_name, description=category_description)
    categories.append(category)

print(f"Created {len(categories)} categories.")

# Lấy danh sách users hiện có
users = list(User.objects.all())
if not users:
    print("No users available. Please create users first.")
else:
    print(f"Using {len(users)} existing users.")

# Tạo dữ liệu cho Post
posts = []
for _ in range(10):
    user = random.choice(users)
    category = random.choice(categories)
    num = random.choice(range(200, 1000))
    post = Post.objects.create(
        author=user,
        title=fake.sentence(),
        content=fake.paragraph(num),
        category=category,
        upvotes=random.randint(0, 50)
    )
    posts.append(post)

print(f"Created {len(posts)} posts.")

# Tạo dữ liệu cho Comment
comments = []
for _ in range(50):
    post = random.choice(posts)
    user = random.choice(users)
    num = random.choice(range(10, 100))
    comment = Comment.objects.create(
        post=post,
        user=user,
        content=fake.sentence(num)
    )
    comments.append(comment)

print(f"Created {len(comments)} comments.")
