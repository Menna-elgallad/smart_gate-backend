# -*- coding: utf-8 -*-

from smart_getenv import getenv


DEBUG = getenv('DEBUG', default=True, type=bool)

PROJECT_NAME = LOGGER_NAME = 'cars'
SECRET_KEY = getenv('SECRET_KEY', default='cars-test')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', default='cars-test')
JWT_ACCESS_TOKEN_EXPIRES = getenv('JWT_ACCESS_TOKEN_EXPIRES', default=219000)
JWT_REFRESH_TOKEN_EXPIRES = getenv('JWT_REFRESH_TOKEN_EXPIRES', default=30)

SQLALCHEMY_DATABASE_URI = getenv(
    'SQLALCHEMY_DATABASE_URI', default='postgresql://postgres:1234@localhost:5432/cars_data')
SQLALCHEMY_TRACK_MODIFICATIONS = getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS', default=True, type=bool)
SERVER_KEY = getenv('SERVER_KEY', default='AAAA29oZ54c:APA91bFPAS7uu7dZ7kr5JZFiMqIGhZJBnkSpbJfsENdnKXvzVnZ6AvOr-efF5vPffbzYnt78JdC82c8zaSq-bmXu3uepnz-ae24Y7tq3ska3BPSNB8HTJJ39Z76I5iK3ZHGT7Qv2uiaQ')
