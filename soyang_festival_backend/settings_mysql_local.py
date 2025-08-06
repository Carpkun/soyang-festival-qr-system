"""
로컬 MySQL 테스트용 Django 설정
"""

from .settings import *

# Debug 모드
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.13']

# 로컬 MySQL 설정 (XAMPP, WAMP 등 사용 시)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'soyang_festival_test',
        'USER': 'root',
        'PASSWORD': '',  # 로컬 MySQL 비밀번호
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# CORS 설정
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
