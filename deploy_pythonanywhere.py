#!/usr/bin/env python3
"""
PythonAnywhere MySQL 배포 스크립트
이 스크립트를 PythonAnywhere Bash 콘솔에서 실행하세요.

사용법:
1. 기본 배포: python3.10 deploy_pythonanywhere.py
2. 데이터 포함: python3.10 deploy_pythonanywhere.py --with-data backup_file.json
"""

import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n🔄 {description}...")
    print(f"실행: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} 완료")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} 실패")
        print(result.stderr)
        return False
    return True

def main():
    print("🌊 소양강문화제 QR 시스템 PythonAnywhere 배포 시작")
    
    # 1. .env 파일 확인
    if not os.path.exists('.env'):
        print("\n⚠️  경고: .env 파일이 없습니다!")
        print(".env.example을 .env로 복사하고 설정을 수정하세요.")
        return False
    else:
        print("\n✅ .env 파일 확인 완료")
    
    # 2. 패키지 설치
    print("\n📦 패키지 설치 중...")
    
    # 2. 패키지 설치
    if not run_command("pip3.10 install --user -r requirements.txt", "패키지 설치"):
        return False
    
    # 3. 데이터베이스 마이그레이션
    if not run_command("python3.10 manage.py migrate --settings=soyang_festival_backend.settings_mysql", "데이터베이스 마이그레이션"):
        return False
    
    # 4. 정적 파일 수집
    if not run_command("python3.10 manage.py collectstatic --noinput --settings=soyang_festival_backend.settings_mysql", "정적 파일 수집"):
        return False
    
    # 5. 샘플 데이터 생성 (선택사항)
    if os.path.exists("create_sample_data.py"):
        run_command("python3.10 create_sample_data.py", "샘플 데이터 생성")
    
    print("\n🎉 배포 완료!")
    print("다음 단계:")
    print("1. PythonAnywhere Web 탭에서 WSGI 설정")
    print("2. Static files 경로 설정")
    print("3. 도메인 확인: yourusername.pythonanywhere.com")

if __name__ == "__main__":
    main()
