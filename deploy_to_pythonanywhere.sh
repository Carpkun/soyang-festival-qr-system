#!/bin/bash

# PythonAnywhere 배포 스크립트
# 사용법: PythonAnywhere 콘솔에서 이 스크립트를 실행

echo "🚀 PythonAnywhere 배포 시작..."

# 1. 프로젝트 디렉터리로 이동
cd ~/soyang-festival-backend
echo "📂 프로젝트 디렉터리: $(pwd)"

# 2. 최신 코드 가져오기
echo "📥 최신 코드 가져오기..."
git pull origin main

# 3. 가상환경 활성화
echo "🐍 가상환경 활성화..."
source venv/bin/activate

# 4. 필요한 디렉터리 생성
echo "📁 디렉터리 생성..."
mkdir -p staticfiles
mkdir -p media
chmod 755 staticfiles
chmod 755 media

# 5. 의존성 설치 (필요시)
echo "📦 의존성 확인..."
pip install -r requirements.txt

# 6. 데이터베이스 마이그레이션
echo "🗄️ 데이터베이스 마이그레이션..."
python manage.py migrate --settings=soyang_festival_backend.settings_pythonanywhere

# 7. static 파일 수집
echo "📦 Static 파일 수집..."
python manage.py collectstatic --noinput --settings=soyang_festival_backend.settings_pythonanywhere

# 8. 현재 설정 확인
echo "🔍 설정 확인..."
python manage.py shell --settings=soyang_festival_backend.settings_pythonanywhere -c "
from django.conf import settings
import os
print('STATIC_ROOT:', settings.STATIC_ROOT)
print('MEDIA_ROOT:', settings.MEDIA_ROOT)
print('Static 폴더 존재:', os.path.exists(settings.STATIC_ROOT))
print('Media 폴더 존재:', os.path.exists(settings.MEDIA_ROOT))
"

echo "✅ 배포 완료!"
echo ""
echo "🌐 다음 단계:"
echo "1. PythonAnywhere Web 탭에서 웹앱 재시작 (Reload 버튼 클릭)"
echo "2. Static Files 설정:"
echo "   - URL: /static/"
echo "   - Directory: /home/ccculture/soyang-festival-backend/staticfiles"
echo "3. Media Files 설정:"
echo "   - URL: /media/"
echo "   - Directory: /home/ccculture/soyang-festival-backend/media"
echo "4. 브라우저에서 https://ccculture.pythonanywhere.com/admin/ 테스트"
