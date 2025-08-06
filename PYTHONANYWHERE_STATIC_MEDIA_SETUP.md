# PythonAnywhere에 Static/Media 파일 설정 적용하기

## 1. PythonAnywhere 콘솔에 접속하여 코드 업데이트

```bash
# 프로젝트 디렉터리로 이동
cd ~/soyang-festival-backend

# 최신 코드 가져오기
git pull origin main
```

## 2. 필요한 디렉터리 생성

```bash
# static 및 media 디렉터리 생성
mkdir -p ~/soyang-festival-backend/staticfiles
mkdir -p ~/soyang-festival-backend/media

# 권한 설정
chmod 755 ~/soyang-festival-backend/staticfiles
chmod 755 ~/soyang-festival-backend/media
```

## 3. Django static 파일 수집

```bash
# 가상환경 활성화 (이미 활성화되어 있다면 생략)
source ~/soyang-festival-backend/venv/bin/activate

# static 파일 수집 (적절한 settings 파일 사용)
python manage.py collectstatic --noinput --settings=soyang_festival_backend.settings_pythonanywhere
```

## 4. PythonAnywhere 웹앱 설정 업데이트

### A. Web 탭에서 Static Files 설정:
- URL: `/static/`
- Directory: `/home/ccculture/soyang-festival-backend/staticfiles`

### B. Media Files 설정 추가:
- URL: `/media/`
- Directory: `/home/ccculture/soyang-festival-backend/media`

## 5. WSGI 파일 업데이트 (필요시)

`/var/www/ccculture_pythonanywhere_com_wsgi.py` 파일에서 settings 모듈 확인:

```python
# 올바른 settings 모듈 사용
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soyang_festival_backend.settings_pythonanywhere')
```

## 6. 웹앱 재시작

PythonAnywhere Web 탭에서 "Reload" 버튼 클릭

## 7. 설정 확인

브라우저에서 다음 URL들이 작동하는지 확인:
- `https://ccculture.pythonanywhere.com/admin/` (Django admin의 CSS가 제대로 로드되는지)
- `https://ccculture.pythonanywhere.com/static/admin/css/base.css` (직접 static 파일 접근)

## 8. 환경 변수 사용 시 (settings_mysql_env.py 사용하는 경우)

Files 탭에서 `.env` 파일 생성 또는 업데이트:

```bash
# ~/soyang-festival-backend/.env
STATIC_ROOT=/home/ccculture/soyang-festival-backend/staticfiles
MEDIA_ROOT=/home/ccculture/soyang-festival-backend/media
DEBUG=False
ALLOWED_HOSTS=ccculture.pythonanywhere.com
# 기타 필요한 환경 변수들...
```

## 문제 해결

### Static 파일이 로드되지 않는 경우:
1. 디렉터리 경로 확인
2. 권한 확인 (`ls -la ~/soyang-festival-backend/`)
3. collectstatic 재실행
4. 웹앱 재시작

### Media 파일 업로드 문제:
1. media 디렉터리 권한 확인
2. Django 설정에서 MEDIA_ROOT, MEDIA_URL 확인
3. 웹앱의 Media Files 설정 확인

### 로그 확인:
- Error log: PythonAnywhere Web 탭의 "Error log" 링크
- Server log: PythonAnywhere Web 탭의 "Server log" 링크

## 완료 후 확인사항

- [ ] Admin 페이지 CSS가 정상 로드됨
- [ ] Static 파일 URL이 정상 작동함
- [ ] Media 파일 업로드가 정상 작동함 (해당하는 경우)
- [ ] 웹앱이 정상적으로 실행됨
