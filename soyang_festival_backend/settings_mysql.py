"""
Django settings for MySQL (PythonAnywhere) deployment
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# PythonAnywhere에서 허용할 호스트
ALLOWED_HOSTS = ['ccculture.pythonanywhere.com', 'localhost', '127.0.0.1']

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ccculture$soyang_festival',
        'USER': 'ccculture', 
        'PASSWORD': 'your-mysql-password',  # 실제 MySQL 비밀번호로 변경
        'HOST': 'ccculture.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/home/ccculture/soyang-festival-qr-system/static'

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ccculture/soyang-festival-qr-system/media'

# Security settings
SECRET_KEY = 'django-secret-lDWW84H2C9eoR5Sc8j_RjWAIZs7gTTNBx6rVB52r-75B09aU_RZnGOeQcyO0CJJRlfdNGWGfjbAA1Zb7NIjjqA'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",  # 프론트엔드 도메인
]

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = True
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
