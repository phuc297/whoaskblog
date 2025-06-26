import random
import os

from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GOOGLE_GENAI_API_KEY)
model_name = "gemini-2.0-flash"


def summarize_post(post_title, post_content):
    prompt = f"Tóm tắt bài viết một cách trung lập, không đưa ý kiến cá nhân. Tiêu đề: {post_title}. Nội dung:\n{post_content}"
    response = client.models.generate_content(
        model=model_name, contents=prompt
    )
    return response.text


def summarize_discussion(comments):
    joined_comments = "\n".join(comments)
    prompt = (
        f"Tóm tắt những gì mọi người đang thảo luận dưới bài viết này một cách trung lập, khách quan:\n{joined_comments}"
    )
    response = client.models.generate_content(
        model=model_name, contents=prompt
    )
    return response.text


def auto_tag_post(post_title, post_content):
    prompt = (
        f"Dựa trên tiêu đề và nội dung bài viết dưới đây, hãy đề xuất các thẻ (tags) ngắn gọn, mang tính mô tả chủ đề. "
        f"Chỉ trả về danh sách các thẻ, phân tách bằng dấu phẩy (nếu không thể trả lời thì đừng trả lời gì cả). \n\nTiêu đề: {post_title}\nNội dung:\n{post_content}"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return [tag.strip() for tag in response.text.split(",")]


def classify_post_topic(post_title, post_content):
    prompt = (
        f"Dựa trên tiêu đề và nội dung sau, hãy phân loại bài viết vào một trong các chủ đề sau: "
        f"[Chính trị, Khoa học, Giải trí, Công nghệ, Xã hội, Giáo dục, Sức khỏe, Kinh tế, Thể thao, Khác]. "
        f"Chỉ trả về tên chủ đề. \n\nTiêu đề: {post_title}\nNội dung:\n{post_content}"
    )
    response = client.models.generate_content(
        model=model_name, contents=prompt
    )
    return response.text.strip()


def analyze_comment_sentiment(comments):
    joined_comments = "\n".join(comments)
    prompt = (
        f"Dựa trên các bình luận sau, đánh giá tổng quan cảm xúc của người dùng là tích cực, tiêu cực, hay trung lập. "
        f"Không liệt kê từng bình luận. Chỉ kết luận tổng quan.\n{joined_comments}"
    )
    response = client.models.generate_content(
        model=model_name, contents=prompt
    )
    return response.text.strip()
