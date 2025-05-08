FROM python:3.9
WORKDIR /web_service
COPY . /web_service
COPY ./people /web_service/people
RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    && pip install --no-cache-dir tensorflow==2.19.0 tf-keras \
    && pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python","web_service.py"]