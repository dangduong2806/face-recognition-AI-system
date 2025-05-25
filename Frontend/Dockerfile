
# Sử dụng image Nginx Alpine
FROM nginx:alpine

# Sao chép toàn bộ nội dung trong thư mục Frontend (bao gồm index.html và nginx.conf)
# COPY . /usr/share/nginx/html/
COPY ./index.html /usr/share/nginx/html/index.html
COPY background.jpg /usr/share/nginx/html/background.jpg
COPY ./login.html /usr/share/nginx/html/login.html


# Sao chép file cấu hình Nginx từ chính thư mục Frontend
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Mở cổng 80
EXPOSE 80

# Chạy Nginx
CMD ["nginx", "-g", "daemon off;"]