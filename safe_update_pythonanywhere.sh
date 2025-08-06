#!/bin/bash

# PythonAnywhere에서 안전하게 코드 업데이트하는 스크립트
# 비밀번호와 같은 로컬 변경사항을 보호합니다

echo "🔄 안전한 코드 업데이트 시작..."

# 현재 디렉터리 확인
cd ~/soyang-festival-qr-system
echo "📂 현재 위치: $(pwd)"

# 로컬 변경사항 백업
echo "💾 로컬 변경사항 백업 중..."
git stash push -m "Local config backup $(date)"

# 최신 코드 가져오기
echo "📥 최신 코드 가져오기..."
git pull origin main

# 가상환경 활성화
echo "🐍 가상환경 활성화..."
source ~/.virtualenvs/soyang-festival/bin/activate || workon soyang-festival

# 의존성 업데이트 (필요시)
echo "📦 의존성 확인..."
pip install -r requirements.txt --quiet

# 마이그레이션 실행
echo "🗄️ 데이터베이스 마이그레이션..."
python manage.py migrate --settings=soyang_festival_backend.settings_env

# static 파일 수집
echo "📦 Static 파일 수집..."
python manage.py collectstatic --noinput --settings=soyang_festival_backend.settings_env

# 백업된 변경사항 복원 여부 확인
echo ""
echo "✅ 코드 업데이트 완료!"
echo ""
echo "🔧 다음 단계:"
echo "1. .env 파일에 비밀번호 설정:"
echo "   nano ~/.env"
echo ""
echo "2. 백업된 설정이 필요하다면 복원:"
echo "   git stash list"
echo "   git stash apply stash@{0}"
echo ""
echo "3. PythonAnywhere Web 탭에서 웹앱 재시작 (Reload 버튼)"
echo ""
echo "4. 설정 확인:"
echo "   python manage.py shell --settings=soyang_festival_backend.settings_env -c \"from django.conf import settings; print('DB:', settings.DATABASES['default']['NAME'])\""
