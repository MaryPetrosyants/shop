FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \ 
    adduser \                                           
        --disabled-password \
        --no-create-home \
        django-user

WORKDIR /shop

EXPOSE 8000

COPY . .

USER django-user

