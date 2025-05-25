# Sử dụng image Python chính thức
FROM python:3.9

# Cài các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy code vào container
COPY . .

# Copy model từ thư mục models vào thư mục làm việc của container
COPY models /app/models

# Cài thư viện Python
RUN pip install --no-cache-dir tensorflow==2.19.0 tf-keras && \
    pip install --no-cache-dir -r requirements.txt

# Lệnh mặc định khi container chạy
CMD ["python", "web_service.py"]
