import os
import json
import random
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from apps.posts.models import Category
from apps.users.models import CustomUser as User

