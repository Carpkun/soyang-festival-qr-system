"""
Django settings for MySQL (PythonAnywhere) deployment
with environment variables support for secure configuration
"""

import os
from .settings import *

# .env 파일 로드 (선택사항)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# PythonAnywhere에서 허용할 호스트
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'ccculture.pythonanywhere.com').split(',')

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ccculture$soyang_festival'),
        'USER': os.getenv('DB_USER', 'ccculture'), 
        'PASSWORD': os.getenv('DB_PASSWORD', 'your-mysql-password'),  # .env에서 가져오거나 기본값
        'HOST': os.getenv('DB_HOST', 'ccculture.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files settings - 올바른 경로로 수정
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', '/home/ccculture/soyang-festival-qr-system/staticfiles')

# Media files settings - 올바른 경로로 수정  
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/home/ccculture/soyang-festival-qr-system/media')

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-secret-lDWW84H2C9eoR5Sc8j_RjWAIZs7gTTNBx6rVB52r-75B09aU_RZnGOeQcyO0CJJRlfdNGWGfjbAA1Zb7NIjjqA')

# CORS settings - 프론트엔드 도메인 추가
CORS_ALLOWED_ORIGINS = [
    os.getenv('FRONTEND_URL', 'https://soyang-festival-qr-system-oh27.vercel.app'),
    "https://ccculture.pythonanywhere.com",
]

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() == 'true'
CORS_ALLOW_CREDENTIALS = True

# MySQL specific optimizations
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Timezone settings
USE_TZ = True
TIME_ZONE = 'Asia/Seoul'

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
