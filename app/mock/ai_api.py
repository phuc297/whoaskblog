import random
from google import genai
from apps.posts.models import Post, Comment
from apps.users.models import CustomUser as User


client = genai.Client(api_key="AIzaSyCp-GK6UKMao3UvqW-nm7SdHdLDNtZWZg0")


def generate_comment(post_title, post_content):
    prompt = f"Generate a comment for the post titled '{post_title}' with the following content:\n\n{post_content}\n\nComment:"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text


def create_comments(n):
    users = User.objects.all()
    posts = Post.objects.all()

    for _ in range(0, n):
        post = random.choice(posts)
        content = generate_comment(post.title, post.content)
        user = random.choice(users)
        comment = Comment(
            post=post,
            user=user,
            content=content
        )
        comment.save()
    print("Good")
