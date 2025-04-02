import random

from faker import Faker

# Chọn một số ngẫu nhiên trong khoảng từ 1 đến 10
num = random.choice(range(10, 50))
print(f"Số được chọn: {num}")
# Khởi tạo Faker
fake = Faker()
print(fake.sentence(num))