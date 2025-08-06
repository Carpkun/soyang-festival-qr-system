"""
Django production settings for PythonAnywhere MySQL deployment
with environment variables for secure configuration
"""

import os
from .settings import *

# python-dotenv가 설치되어 있다면 사용
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Production specific settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-secret-fallback-key')

# Allowed hosts for production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'ccculture.pythonanywhere.com').split(',')

# MySQL Database configuration for PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ccculture$soyang_festival'),
        'USER': os.getenv('DB_USER', 'ccculture'),
        'PASSWORD': os.getenv('DB_PASSWORD'),  # 필수 환경변수
        'HOST': os.getenv('DB_HOST', 'ccculture.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', '/home/ccculture/soyang-festival-qr-system/staticfiles')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/home/ccculture/soyang-festival-qr-system/media')

# CORS settings for production
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://soyang-festival-qr-system-oh27.vercel.app')
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "https://ccculture.pythonanywhere.com",  # 백엔드 자체
]

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() == 'true'
CORS_ALLOW_CREDENTIALS = True

# MySQL specific optimizations
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Timezone settings
USE_TZ = True
TIME_ZONE = 'Asia/Seoul'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
