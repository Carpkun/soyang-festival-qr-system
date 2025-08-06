# 🌐 프론트엔드 배포 가이드

## 🎯 배포 전 체크리스트

- [x] API 서비스 URL이 `https://ccculture.pythonanywhere.com/api`로 설정됨
- [x] QR 코드 생성이 올바른 URL 형태로 통일됨
- [x] 백엔드 CORS 설정이 프론트엔드 도메인을 허용하도록 설정됨

## 🚀 배포 방법 (추천순)

### 1. Vercel 배포 (가장 추천) ⭐

**장점:**
- 무료 SSL 제공
- 자동 빌드 및 배포
- CDN 지원으로 빠른 로딩
- GitHub 연동 시 자동 배포

**배포 단계:**

1. **[Vercel.com](https://vercel.com) 가입**

2. **프로젝트 연결**
   ```
   - "Add New Project" 클릭
   - GitHub에서 "soyang-festival-qr-system" 선택
   - "Import" 클릭
   ```

3. **설정 구성**
   ```
   Framework Preset: Vite
   Root Directory: soyang-festival-frontend
   Build Command: npm run build (자동 감지)
   Output Directory: dist (자동 감지)
   Install Command: npm install (자동 감지)
   ```

4. **배포**
   - "Deploy" 클릭
   - 3-5분 후 배포 완료

5. **도메인 확인**
   - `https://your-project-name.vercel.app` 형태로 제공됨

### 2. Netlify 배포

**배포 단계:**

1. **[Netlify.com](https://netlify.com) 가입**

2. **사이트 생성**
   ```
   - "Add new site" > "Import from Git"
   - GitHub에서 저장소 선택
   ```

3. **빌드 설정**
   ```
   Base directory: soyang-festival-frontend
   Build command: npm run build
   Publish directory: soyang-festival-frontend/dist
   ```

4. **배포**
   - "Deploy site" 클릭

### 3. GitHub Pages 배포

**사전 설정:**
- GitHub 저장소의 Settings > Pages에서 Source를 "GitHub Actions"로 설정

**자동 배포:**
- `.github/workflows/deploy-frontend.yml` 파일이 이미 생성됨
- `main` 브랜치에 푸시하면 자동으로 배포됨

## 🔧 배포 후 설정

### 1. 백엔드 CORS 설정 업데이트

PythonAnywhere의 Django 설정에서 프론트엔드 도메인을 허용해야 합니다:

```python
# soyang_festival_backend/settings_mysql.py 수정
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",  # Vercel 도메인
    "https://your-username.github.io",          # GitHub Pages 도메인
    "https://your-site-name.netlify.app",       # Netlify 도메인
]

# 개발 중에만 모든 오리진 허용 (프로덕션에서는 제거 고려)
CORS_ALLOW_ALL_ORIGINS = True
```

### 2. QR 코드 테스트

배포 완료 후 다음을 확인:

1. **QR 코드 생성 테스트**
   - 관리자 페이지(`https://your-domain.com/?admin=true`) 접속
   - 부스 QR 코드 생성 확인

2. **QR 코드 스캔 테스트**
   - 생성된 QR 코드 스캔
   - 올바른 페이지로 이동하는지 확인

3. **API 연동 테스트**
   - 닉네임 등록
   - 스탬프 수집
   - 통계 확인

## 📱 모바일 최적화

- 반응형 디자인이 적용되어 모바일에서도 정상 작동
- QR 코드 스캔 기능은 HTTPS 환경에서만 작동 (배포 환경에서는 문제없음)

## 🔍 문제 해결

### CORS 오류 발생 시
1. 백엔드 CORS 설정에 프론트엔드 도메인 추가
2. PythonAnywhere에서 웹앱 재시작

### API 통신 오류 시
1. 브라우저 개발자 도구에서 네트워크 탭 확인
2. API 엔드포인트 URL 올바른지 확인
3. 백엔드 서버 상태 확인

### QR 스캐너 작동하지 않을 시
1. HTTPS 환경에서 접속하는지 확인
2. 카메라 권한 허용했는지 확인
3. 모바일 브라우저에서 테스트

## 📝 배포 완료 후 확인사항

- [ ] 프론트엔드 정상 배포됨
- [ ] 백엔드 API 통신 정상 작동
- [ ] QR 코드 생성 기능 정상
- [ ] QR 코드 스캔 기능 정상
- [ ] 스탬프 수집 시스템 정상
- [ ] 관리자 기능 정상
- [ ] 모바일 환경에서 정상 작동

## 🎉 배포 완료!

배포가 완료되면 다음과 같이 시스템이 구성됩니다:

- **프론트엔드**: `https://your-domain.com` (Vercel/Netlify/GitHub Pages)
- **백엔드 API**: `https://ccculture.pythonanywhere.com/api`
- **관리자**: `https://ccculture.pythonanywhere.com/admin`
- **QR 시스템**: 완전 통합되어 작동

## 📞 지원

배포 중 문제가 발생하면:
1. GitHub Issues에 문제 보고
2. 로그 및 오류 메시지 포함
3. 브라우저 개발자 도구 스크린샷 첨부
