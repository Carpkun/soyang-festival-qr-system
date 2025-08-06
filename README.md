# 소양강문화제 QR 스탬프 랠리 시스템

## 프로젝트 구조
- **백엔드**: Django + PostgreSQL + Django REST Framework
- **프론트엔드**: React + TypeScript + Vite
- **QR 스캔**: @zxing/library

## 로컬 개발 환경 실행

### 백엔드 실행
```bash
cd qr
python manage.py runserver 0.0.0.0:8000
```

### 프론트엔드 실행  
```bash
cd soyang-festival-frontend
npm install
npm run dev
```

## 환경 설정

### 환경 변수 설정 (중요!)
배포 전에 `.env` 파일을 생성하여 민감정보를 설정하세요:

```bash
# .env 파일 생성 (루트 디렉토리에)
cp .env.example .env
```

`.env` 파일에서 다음 값들을 실제 값으로 변경:
- `DJANGO_SECRET_KEY`: 강력한 시크릿 키로 변경
- `DB_PASSWORD`: 실제 MySQL 비밀번호로 변경
- 기타 필요한 설정들

### 스탬프 목표 개수
현재 **5개** 부스 스탬프 수집으로 설정되어 있습니다.

## 무료 배포 방법 (MySQL + PythonAnywhere)

### 1. 백엔드 배포 (PythonAnywhere - 무료, 슬립 없음)
1. [PythonAnywhere.com](https://www.pythonanywhere.com) 가입
2. MySQL 데이터베이스 생성
3. GitHub 저장소 연결
4. `.env` 파일 설정 (위 참조)
5. `settings_mysql.py` 설정 사용:
   ```bash
   # PythonAnywhere에서 실행
   python manage.py migrate --settings=soyang_festival_backend.settings_mysql
   python manage.py collectstatic --settings=soyang_festival_backend.settings_mysql
   ```

### 3. 프론트엔드 배포 (Vercel - 무료)
1. [Vercel.com](https://vercel.com) 가입  
2. GitHub 저장소 연결
3. 빌드 설정:
   - **Build Command**: `cd soyang-festival-frontend && npm run build`
   - **Output Directory**: `soyang-festival-frontend/dist`

### 4. 도메인 설정
배포 완료 후:
1. `soyang-festival-frontend/src/services/api.ts`에서 백엔드 URL 업데이트
2. `settings_production.py`에서 CORS_ALLOWED_ORIGINS에 프론트엔드 URL 추가

## 기능

### 사용자 기능
- 닉네임 등록
- QR 코드 스캔하여 스탬프 획득
- 스탬프 수집 현황 확인

### 관리자 기능 (`?admin=true`)
- 부스 관리
- QR 코드 생성 및 출력
- 참여자 통계 대시보드

## 모바일 테스트
스마트폰에서 같은 네트워크로 접속:
- 메인: `http://[IP]:5173/`
- 관리자: `http://[IP]:5173/?admin=true`
