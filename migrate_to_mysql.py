#!/usr/bin/env python3
"""
PostgreSQL → MySQL 데이터 마이그레이션 스크립트
"""

import os
import django
import json
from datetime import datetime

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soyang_festival_backend.settings')
django.setup()

from stampapp.models import Booth, Participant, Stamp

def export_postgresql_data():
    """현재 PostgreSQL 데이터를 JSON으로 내보내기"""
    
    print("🔄 PostgreSQL 데이터 내보내기 중...")
    
    data = {
        'booths': [],
        'participants': [],
        'stamps': []
    }
    
    # 부스 데이터
    for booth in Booth.objects.all():
        data['booths'].append({
            'id': str(booth.id),
            'name': booth.name,
            'description': booth.description,
            'is_active': booth.is_active,
            'created_at': booth.created_at.isoformat()
        })
    
    # 참여자 데이터
    for participant in Participant.objects.all():
        data['participants'].append({
            'id': str(participant.id),
            'nickname': participant.nickname,
            'created_at': participant.created_at.isoformat()
        })
    
    # 스탬프 데이터
    for stamp in Stamp.objects.all():
        data['stamps'].append({
            'id': stamp.id,
            'participant_id': str(stamp.participant.id),
            'booth_id': str(stamp.booth.id),
            'created_at': stamp.created_at.isoformat()
        })
    
    # JSON 파일로 저장
    filename = f'postgresql_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 데이터 내보내기 완료: {filename}")
    print(f"   - 부스: {len(data['booths'])}개")
    print(f"   - 참여자: {len(data['participants'])}개")
    print(f"   - 스탬프: {len(data['stamps'])}개")
    
    return filename

def import_to_mysql(backup_file, use_mysql_settings=True):
    """
    백업 데이터를 MySQL로 가져오기
    (PythonAnywhere에서 MySQL 설정 후 실행)
    """
    
    print(f"🔄 {backup_file}에서 MySQL로 데이터 가져오기 중...")
    
    # 기존 데이터 삭제 (주의!)
    Stamp.objects.all().delete()
    Participant.objects.all().delete()  
    Booth.objects.all().delete()
    
    # JSON 파일 읽기
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 부스 데이터 가져오기
    booth_map = {}
    for booth_data in data['booths']:
        booth = Booth.objects.create(
            id=booth_data['id'],
            name=booth_data['name'],
            description=booth_data['description'],
            is_active=booth_data['is_active']
        )
        booth_map[booth_data['id']] = booth
        print(f"   ✅ 부스 생성: {booth.name}")
    
    # 참여자 데이터 가져오기
    participant_map = {}
    for participant_data in data['participants']:
        participant = Participant.objects.create(
            id=participant_data['id'],
            nickname=participant_data['nickname']
        )
        participant_map[participant_data['id']] = participant
        print(f"   ✅ 참여자 생성: {participant.nickname}")
    
    # 스탬프 데이터 가져오기
    for stamp_data in data['stamps']:
        participant = participant_map[stamp_data['participant_id']]
        booth = booth_map[stamp_data['booth_id']]
        
        stamp = Stamp.objects.create(
            participant=participant,
            booth=booth
        )
        print(f"   ✅ 스탬프 생성: {participant.nickname} - {booth.name}")
    
    print("🎉 MySQL 데이터 가져오기 완료!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'import':
        # 가져오기 모드
        backup_file = input("백업 파일명을 입력하세요: ")
        import_to_mysql(backup_file)
    else:
        # 내보내기 모드
        export_postgresql_data()
