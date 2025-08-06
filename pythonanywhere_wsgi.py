"""
PythonAnywhere WSGI 설정 파일
이 내용을 PythonAnywhere의 WSGI configuration file에 복사하세요.
"""

import os
import sys

# 프로젝트 경로 설정 (실제 사용자명으로 변경)
project_home = '/home/yourusername/soyang-festival-backend'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Django 설정 모듈 지정
os.environ['DJANGO_SETTINGS_MODULE'] = 'soyang_festival_backend.settings_mysql'

# Django WSGI 애플리케이션
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
