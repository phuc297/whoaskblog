import os
import json
import random
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from apps.posts.models import Category
from apps.users.models import CustomUser as User

categories = {
    "Thời sự": 1,
    "Thể thao": 2,
    "Giải trí": 3,
    "Kinh doanh": 4,
    "Pháp luật": 5,
}

def get_article_links(category_url, num_articles=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Không thể truy cập {category_url}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("h3", class_="title-news", limit=num_articles)
    links = [a.a["href"] for a in articles if a.a]
    return links

def get_article_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Không thể lấy nội dung từ {url}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", class_="title-detail").text.strip()
    paragraphs = soup.find_all("p", class_="Normal")
    content = "".join([f"<p>{p.text.strip()}</p>\n" for p in paragraphs])
    return title, content

def crawl_articles():
    articles_data = []
    post_id = 1
    users = User.objects.all().filter(is_superuser=False)
    for category_name, category_id in categories.items():
        print(f"📂 Đang crawl chuyên mục: {category_name}")

        article_links = get_article_links(f"https://vnexpress.net/{slugify(category_name)}")
        category_object = Category.objects.get(name=category_name)
        for article_url in article_links:
            article = get_article_content(article_url)
            if article:
                title, content = article
                articles_data.append({
                    "model": "apps.post",
                    "pk": post_id,
                    "fields": {
                        "author": random.choice(users).id,
                        "title": title,
                        "content": content,
                        "created_at": "2025-02-16T10:00:00Z",
                        "updated_at": "2025-02-16T10:00:00Z",
                        "category": category_object.id,
                        "upvotes": 0,
                        "slug": slugify(title)
                    }
                })
                post_id += 1
                print(f"✅ Đã crawl: {title}")

    with open("articles.json", "w", encoding="utf-8") as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

    print("\n🎉 Crawl hoàn tất! Dữ liệu đã được lưu vào `articles.json`.")

crawl_articles()
