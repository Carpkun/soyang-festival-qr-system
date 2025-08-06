"""
Django settings for MySQL (PythonAnywhere) deployment with environment variables
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# PythonAnywhere에서 허용할 호스트
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'yourusername.pythonanywhere.com').split(',')

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'yourusername$soyang_festival'),
        'USER': os.environ.get('DB_USER', 'yourusername'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-mysql-password'),
        'HOST': os.environ.get('DB_HOST', 'yourusername.mysql.pythonanywhere-services.com'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/yourusername/soyang-festival-backend/static')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/yourusername/soyang-festival-backend/media')

# Security settings - 환경 변수에서 가져오기
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-secret-lDWW84H2C9eoR5Sc8j_RjWAIZs7gTTNBx6rVB52r-75B09aU_RZnGOeQcyO0CJJRlfdNGWGfjbAA1Zb7NIjjqA')

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://your-frontend-domain.vercel.app').split(',')

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'
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
