"""
Django production settings for soyang_festival_backend project.
"""

import os
import dj_database_url
from decouple import config

from .settings import *

# Production specific settings
DEBUG = config('DEBUG', default=False, cast=bool)

# Security settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')

# Allowed hosts for production
ALLOWED_HOSTS = ['*']  # 배포 후 실제 도메인으로 제한

# Database configuration for production
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",  # 프론트엔드 배포 URL로 변경
]

# 개발 중에는 모든 오리진 허용
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOW_CREDENTIALS = True

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
