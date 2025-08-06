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

## 무료 배포 방법 (MySQL + PythonAnywhere)

### 1. 백엔드 배포 (PythonAnywhere - 무료, 슬립 없음)
1. [PythonAnywhere.com](https://www.pythonanywhere.com) 가입
2. MySQL 데이터베이스 생성
3. GitHub 저장소 연결
4. 자동 배포 스크립트 실행:
   ```bash
   python3.10 deploy_pythonanywhere.py
   ```
5. 설정 파일 수정 (`settings_mysql.py`):
   - 사용자명, 비밀번호, 도메인 설정

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
