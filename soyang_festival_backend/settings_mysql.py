"""
Django settings for MySQL (PythonAnywhere) deployment
소양강문화제 QR 스탬프 랠리 시스템 - 통합 배포 설정
"""

import os
from pathlib import Path

# .env 파일 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-this-secret-key-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'ccculture.pythonanywhere.com').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'stampapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'soyang_festival_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'soyang_festival_backend.wsgi.application'

# MySQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ccculture$soyang_festival'),
        'USER': os.getenv('DB_USER', 'ccculture'),
        'PASSWORD': os.getenv('DB_PASSWORD'),  # .env 파일에서 필수로 가져와야 함
        'HOST': os.getenv('DB_HOST', 'ccculture.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', '/home/ccculture/soyang-festival-qr-system/staticfiles')

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/home/ccculture/soyang-festival-qr-system/media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    os.getenv('FRONTEND_URL', 'https://soyang-festival-qr-system-oh27.vercel.app'),
    "https://ccculture.pythonanywhere.com",
]

CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'
CORS_ALLOW_CREDENTIALS = True

# Django REST Framework settings (축제 현장 최적화)
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,  # 축제 현장 부하 분산
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',  # 익명 사용자 분당 60회 (QR 스캔 고려)
        'user': '120/minute'  # 등록 사용자 분당 120회
    },
}

# 유료 플랜 최적화 설정
# 데이터베이스 연결 최적화 (유료 플랜은 연결 재사용 가능)
DATABASES['default']['CONN_MAX_AGE'] = 60  # 60초 동안 연결 재사용
DATABASES['default']['OPTIONS'].update({
    'connect_timeout': 10,
    'read_timeout': 10,
    'write_timeout': 10,
})

# 세션 설정 최적화 (안정성을 위해 DB 기반 사용)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_CACHE_ALIAS = 'default'  # DB 기반에서는 불필요
SESSION_COOKIE_AGE = 3600  # 1시간
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 캐시 설정 (메모리 기반)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5분
        'OPTIONS': {
            'MAX_ENTRIES': 100,
        }
    }
}

# 로깅 최적화 (에러만 로그)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',  # ERROR 레벨만 로깅
    },
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Production security settings (HTTPS 관련)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
