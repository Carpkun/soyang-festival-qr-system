"""
Django settings with environment variables support
환경변수를 지원하는 간단한 설정 파일
"""

import os
from .settings import *

# .env 파일이 있다면 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# DEBUG 모드
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 허용 호스트
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'ccculture.pythonanywhere.com').split(',')

# 비밀키
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')

# MySQL 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ccculture$soyang_festival'),
        'USER': os.getenv('DB_USER', 'ccculture'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'fallback-password'),
        'HOST': os.getenv('DB_HOST', 'ccculture.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static/Media 파일 설정
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', '/home/ccculture/soyang-festival-qr-system/staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/home/ccculture/soyang-festival-qr-system/media')

# CORS 설정
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://soyang-festival-qr-system-oh27.vercel.app')
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "https://ccculture.pythonanywhere.com",
]

CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() == 'true'
CORS_ALLOW_CREDENTIALS = True

# MySQL 최적화
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# 시간대 설정
USE_TZ = True
TIME_ZONE = 'Asia/Seoul'

# 보안 설정
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
