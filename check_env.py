#!/usr/bin/env python3
"""
PythonAnywhere 환경 설정 확인 스크립트
이 스크립트를 PythonAnywhere Bash 콘솔에서 실행하세요.
"""

import os
import sys

def check_env():
    print("🔍 환경 설정 확인 중...")
    
    # 1. .env 파일 확인
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ {env_file} 파일이 존재합니다")
        
        # .env 파일 내용 확인 (비밀번호는 마스킹)
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        print("\n📋 .env 파일 내용:")
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if 'PASSWORD' in line:
                    key = line.split('=')[0]
                    print(f"  {key}=***MASKED***")
                else:
                    print(f"  {line}")
    else:
        print(f"❌ {env_file} 파일이 없습니다!")
        return False
    
    # 2. 환경 변수 로드 테스트
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("\n✅ python-dotenv 라이브러리 로드 성공")
    except ImportError:
        print("\n❌ python-dotenv 라이브러리가 설치되지 않았습니다")
        return False
    
    # 3. 중요한 환경 변수들 확인
    print("\n🔑 환경 변수 확인:")
    important_vars = [
        'DJANGO_SECRET_KEY',
        'DB_NAME', 
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT'
    ]
    
    for var in important_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var or 'SECRET' in var:
                print(f"  {var}: ***SET*** (길이: {len(value)})")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: ❌ NOT SET")
    
    # 4. MySQL 연결 테스트
    print("\n🗄️  MySQL 연결 테스트:")
    try:
        import MySQLdb
        
        db_config = {
            'host': os.getenv('DB_HOST', 'ccculture.mysql.pythonanywhere-services.com'),
            'user': os.getenv('DB_USER', 'ccculture'),
            'passwd': os.getenv('DB_PASSWORD'),
            'db': os.getenv('DB_NAME', 'ccculture$soyang_festival'),
            'port': int(os.getenv('DB_PORT', '3306'))
        }
        
        if not db_config['passwd']:
            print("❌ DB_PASSWORD가 설정되지 않았습니다!")
            return False
            
        conn = MySQLdb.connect(**db_config)
        print("✅ MySQL 연결 성공!")
        conn.close()
        
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return False
    
    print("\n🎉 모든 환경 설정이 올바릅니다!")
    return True

if __name__ == "__main__":
    if check_env():
        print("\n✅ Django 서버를 재시작할 수 있습니다.")
    else:
        print("\n❌ 환경 설정을 수정한 후 다시 시도하세요.")
