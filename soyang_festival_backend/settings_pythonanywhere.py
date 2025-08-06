"""
Django settings for PythonAnywhere deployment
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# PythonAnywhere에서 허용할 호스트
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']  # 실제 PythonAnywhere 사용자명으로 변경

# Database - PythonAnywhere MySQL (무료 계정)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$soyang_festival',  # 실제 사용자명으로 변경
        'USER': 'yourusername',  # 실제 사용자명으로 변경
        'PASSWORD': 'your-mysql-password',  # PythonAnywhere MySQL 비밀번호
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',  # 실제 사용자명으로 변경
        'PORT': '3306',
    }
}

# PostgreSQL을 사용하려면 (외부 서비스 필요)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'soyang_festival',
#         'USER': 'username',
#         'PASSWORD': 'password',
#         'HOST': 'external-postgres-host',
#         'PORT': '5432',
#     }
# }

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/home/ccculture/soyang-festival-backend/staticfiles'  # collectstatic으로 수집된 파일들

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ccculture/soyang-festival-backend/media'  # 사용자 업로드 파일들

# Security settings
SECRET_KEY = 'your-secret-key-here'  # 강력한 비밀키로 변경

# CORS settings - 프론트엔드 배포 후 실제 도메인으로 변경
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",
]

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
