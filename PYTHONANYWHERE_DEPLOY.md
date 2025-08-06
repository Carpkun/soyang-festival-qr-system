# 🎪 소양강문화제 QR 시스템 - PythonAnywhere MySQL 배포 가이드

## 📋 배포 전 준비사항

### 1. 현재 PostgreSQL 데이터 백업
```bash
# 로컬에서 실행
python migrate_to_mysql.py
# 백업 파일(postgresql_backup_XXXXXX.json) 생성됨
```

### 2. 필요한 정보 준비
- **PythonAnywhere 사용자명**: `your_username`
- **MySQL 비밀번호**: PythonAnywhere에서 설정
- **SECRET_KEY**: 강력한 비밀키

## 🚀 단계별 배포 과정

### 1단계: PythonAnywhere 계정 설정
1. **[PythonAnywhere.com](https://www.pythonanywhere.com)** 가입
2. **Beginner 계정** 선택 (무료)

### 2단계: MySQL 데이터베이스 생성
1. **Databases 탭** 클릭
2. **Create a database** 
   - Database name: `your_username$soyang_festival`
   - Password: 강력한 비밀번호 설정 및 기록

### 3단계: 코드 업로드
**방법 A: Git 사용 (권장)**
```bash
# PythonAnywhere Bash 콘솔에서
cd ~
git clone https://github.com/your-username/soyang-festival-backend.git
cd soyang-festival-backend
```

**방법 B: 파일 직접 업로드**
- Files 탭에서 프로젝트 파일들 업로드

### 4단계: 설정 파일 수정
`settings_mysql.py` 파일에서 다음 값들을 실제 값으로 변경:

```python
# 실제 사용자명으로 변경
ALLOWED_HOSTS = ['your_username.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_username$soyang_festival',  # ← 실제 사용자명
        'USER': 'your_username',  # ← 실제 사용자명
        'PASSWORD': 'your-mysql-password',  # ← 실제 MySQL 비밀번호
        'HOST': 'your_username.mysql.pythonanywhere-services.com',  # ← 실제 사용자명
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# 강력한 비밀키로 변경
SECRET_KEY = 'your-super-secret-key-here'

# 실제 경로로 변경
STATIC_ROOT = '/home/your_username/soyang-festival-backend/static'
MEDIA_ROOT = '/home/your_username/soyang-festival-backend/media'
```

### 5단계: 자동 배포 실행
```bash
# PythonAnywhere Bash 콘솔에서
cd ~/soyang-festival-backend
python3.10 deploy_pythonanywhere.py
```

### 6단계: 데이터 마이그레이션
```bash
# 백업 파일을 PythonAnywhere에 업로드 후
cd ~/soyang-festival-backend

# Django 설정을 MySQL로 변경하여 데이터 import
DJANGO_SETTINGS_MODULE=soyang_festival_backend.settings_mysql python3.10 migrate_to_mysql.py import
# 백업 파일명 입력: postgresql_backup_XXXXXX.json
```

### 7단계: 웹 애플리케이션 설정
1. **Web 탭** 클릭
2. **"Add a new web app"** 클릭
3. **Manual configuration** 선택
4. **Python 3.10** 선택

**WSGI Configuration File 편집:**
```python
import os
import sys

# 프로젝트 경로 (실제 사용자명으로 변경)
project_home = '/home/your_username/soyang-festival-backend'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Django 설정
os.environ['DJANGO_SETTINGS_MODULE'] = 'soyang_festival_backend.settings_mysql'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static Files 설정:**
- URL: `/static/`
- Directory: `/home/your_username/soyang-festival-backend/static/`

### 8단계: 웹 앱 리로드 및 테스트
1. **"Reload" 버튼** 클릭
2. **your_username.pythonanywhere.com** 접속 테스트
3. API 테스트: `your_username.pythonanywhere.com/api/booths/`

## 🌐 프론트엔드 배포 (Vercel)

### 1. API URL 업데이트
`soyang-festival-frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your_username.pythonanywhere.com/api'  // 실제 사용자명
  : 'http://192.168.0.13:8000/api';
```

### 2. Vercel 배포
1. **[Vercel.com](https://vercel.com)** 가입
2. GitHub 저장소 연결
3. 빌드 설정:
   - **Root Directory**: `soyang-festival-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3. CORS 설정 업데이트
백엔드 `settings_mysql.py`에서:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-project.vercel.app",  # 실제 Vercel 도메인
]
```

## ✅ 배포 완료 확인

### 백엔드 테스트
- ✅ `https://your_username.pythonanywhere.com/` - API 루트
- ✅ `https://your_username.pythonanywhere.com/api/booths/` - 부스 목록
- ✅ `https://your_username.pythonanywhere.com/admin/` - Django 관리자

### 프론트엔드 테스트  
- ✅ `https://your-project.vercel.app/` - 메인 페이지
- ✅ `https://your-project.vercel.app/?admin=true` - 관리자 모드

## 🎯 최종 URL 정리
배포 완료 후 접속 가능한 주소들:

- **사용자 메인**: `https://your-project.vercel.app/`
- **관리자 페이지**: `https://your-project.vercel.app/?admin=true`
- **백엔드 API**: `https://your_username.pythonanywhere.com/api/`
- **Django Admin**: `https://your_username.pythonanywhere.com/admin/`

## 🛠 문제 해결

### MySQL 연결 오류
```bash
# MySQL 클라이언트 재설치
pip3.10 install --user --force-reinstall mysqlclient
```

### Static Files 404 오류  
```bash
# Static files 재수집
python3.10 manage.py collectstatic --clear --noinput --settings=soyang_festival_backend.settings_mysql
```

### CORS 오류
`settings_mysql.py`에서 일시적으로:
```python
CORS_ALLOW_ALL_ORIGINS = True  # 테스트용
```

## 🎉 완료!
소양강문화제 QR 스탬프 랠리 시스템이 성공적으로 배포되었습니다!

- **24시간 무중단 서비스** ✅
- **즉시 QR 스캔 응답** ✅  
- **실시간 관리자 대시보드** ✅
- **완전 무료 호스팅** ✅
