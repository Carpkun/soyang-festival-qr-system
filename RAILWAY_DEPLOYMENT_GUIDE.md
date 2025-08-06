# Railway 배포 가이드 (1,000명 접속 대응)

## 🚀 Railway란?
- 무료 티어로도 충분한 트래픽 처리 가능
- PostgreSQL 데이터베이스 무료 제공
- 자동 배포 및 스케일링
- 월 500시간 무료 실행 시간

## 📋 배포 준비

### 1. Railway 계정 생성
1. [Railway.app](https://railway.app) 접속
2. GitHub 계정으로 로그인
3. 새 프로젝트 생성

### 2. 필요한 파일 준비

#### `railway.toml` (프로젝트 루트에 생성)
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python manage.py migrate --settings=soyang_festival_backend.settings_railway && python manage.py collectstatic --noinput --settings=soyang_festival_backend.settings_railway && gunicorn soyang_festival_backend.wsgi:application --bind 0.0.0.0:$PORT --settings=soyang_festival_backend.settings_railway"
healthcheckPath = "/admin/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[variables]
DJANGO_SETTINGS_MODULE = "soyang_festival_backend.settings_railway"
```

#### `requirements.txt`에 추가
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### 3. Railway 전용 설정 파일 생성

#### `settings_railway.py`
```python
"""
Railway 배포용 Django 설정
"""
import os
import dj_database_url
from .settings import *

# Railway 환경 변수에서 설정 읽기
DEBUG = False
ALLOWED_HOSTS = ['*']

# 데이터베이스 설정 (Railway PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# 시크릿 키
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# 정적 파일 설정
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 미디어 파일 설정 (클라우드 스토리지 사용 권장)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS 설정
CORS_ALLOWED_ORIGINS = [
    os.environ.get('FRONTEND_URL', 'https://soyang-festival-qr-system-oh27.vercel.app'),
]

# 보안 설정
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

## 🔧 배포 단계

### 1. GitHub에서 Railway 연결
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 프로젝트 저장소 선택

### 2. 환경 변수 설정
Railway 프로젝트 → Variables 탭에서 설정:
```
DJANGO_SECRET_KEY=강력한-시크릿-키
FRONTEND_URL=https://soyang-festival-qr-system-oh27.vercel.app
```

### 3. PostgreSQL 데이터베이스 추가
1. Railway 프로젝트에서 "Add Service"
2. "PostgreSQL" 선택
3. 자동으로 `DATABASE_URL` 환경 변수 생성됨

### 4. 도메인 설정
1. Railway 프로젝트 → Settings → Domains
2. 커스텀 도메인 설정 (선택사항)

## 💰 비용 예상

### 무료 티어
- **실행 시간**: 월 500시간
- **1,000명/일 기준**: 충분히 처리 가능
- **데이터베이스**: PostgreSQL 무료 제공

### 유료 ($5/월)
- **무제한 실행 시간**
- **더 많은 리소스**
- **우선 지원**

## 🔄 기존 데이터 마이그레이션

### PythonAnywhere → Railway 데이터 이전
```bash
# 1. PythonAnywhere에서 데이터 백업
python manage.py dumpdata --settings=soyang_festival_backend.settings_mysql > backup.json

# 2. Railway에서 데이터 복원
python manage.py loaddata backup.json --settings=soyang_festival_backend.settings_railway
```

## 📈 성능 최적화 팁

1. **데이터베이스 쿼리 최적화**
2. **캐싱 활용**
3. **정적 파일 CDN 사용**
4. **이미지 최적화**

Railway는 1,000명 접속을 무료로도 충분히 처리할 수 있는 플랫폼입니다!
