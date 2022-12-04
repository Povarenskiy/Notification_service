FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
WORKDIR /code/notification_service
