"""
PythonAnywhere 유료 플랜 최적화 설정
Hacker Plan ($5/월) 기준으로 최적화
"""

from .settings_mysql import *

# 유료 플랜 전용 최적화 설정
DEBUG = False

# 더 많은 동시 접속 처리를 위한 설정
DATABASES['default']['CONN_MAX_AGE'] = 60  # 연결 재사용 (유료 플랜에서는 가능)
DATABASES['default']['OPTIONS'].update({
    'connect_timeout': 10,
    'read_timeout': 10,
    'write_timeout': 10,
    'pool_timeout': 20,
    'pool_recycle': 3600,
})

# 향상된 캐시 설정
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # 더 많은 캐시 엔트리
        }
    }
}

# 세션 최적화 (유료 플랜용)
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 7200  # 2시간 (더 긴 세션)

# 정적 파일 캐싱 강화
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# API 응답 최적화
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 익명 사용자 시간당 100회
        'user': '1000/hour'  # 등록 사용자 시간당 1000회
    },
    'PAGE_SIZE': 100,  # 페이지 크기 증가
})

# 로깅 개선 (유료 플랜에서는 더 상세한 로깅 가능)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/home/ccculture/logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'stampapp': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# 보안 강화 (유료 플랜 전용)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# 성능 모니터링 (선택사항)
# Django Debug Toolbar는 유료 플랜에서만 권장
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

print("✅ PythonAnywhere 유료 플랜 최적화 설정 로드됨")
