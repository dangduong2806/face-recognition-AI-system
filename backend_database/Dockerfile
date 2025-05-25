FROM python:3.9

WORKDIR /app

# Copy file requirements và file .whl của TensorFlow vào image
COPY requirements.txt .
COPY tensorflow-2.19.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .
COPY .env .env

# Copy model từ thư mục models vào thư mục làm việc của container
COPY models /app/models
# Cài đặt hệ thống + pip + các gói Python (ưu tiên dùng .whl TensorFlow đã tải)
RUN apt-get update && apt-get install -y libgl1 && \
    pip install --upgrade pip && \
    pip install --no-cache-dir tensorflow-2.19.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl tf-keras && \
    pip install -r requirements.txt

# Sau khi cài xong mới copy source code vào
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
