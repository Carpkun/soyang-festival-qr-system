"""
Django settings for MySQL (PythonAnywhere) deployment
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# PythonAnywhere에서 허용할 호스트
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']  # 실제 사용자명으로 변경

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$soyang_festival',  # 실제 사용자명으로 변경
        'USER': 'yourusername',  # 실제 사용자명으로 변경
        'PASSWORD': 'your-mysql-password',  # MySQL 비밀번호
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',  # 실제 사용자명으로 변경
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
STATIC_ROOT = '/home/yourusername/soyang-festival-backend/static'  # 실제 경로로 변경

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/soyang-festival-backend/media'  # 실제 경로로 변경

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
