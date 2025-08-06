#!/usr/bin/env python
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soyang_festival_backend.settings')
django.setup()

from stampapp.models import Booth

def create_sample_booths():
    """샘플 부스 데이터를 생성합니다."""
    booth_names = [
        "전통 음식 체험",
        "도자기 만들기",
        "한복 체험",
        "전통 악기 연주",
        "민속놀이 체험",
        "서예 체험",
        "떡 만들기",
        "천연 비누 만들기"
    ]
    
    created_booths = []
    for name in booth_names:
        booth, created = Booth.objects.get_or_create(name=name)
        if created:
            created_booths.append(booth)
            print(f"✓ 부스 '{name}' 생성됨 (ID: {booth.id})")
        else:
            print(f"- 부스 '{name}' 이미 존재함")
    
    print(f"\n총 {len(created_booths)}개의 새로운 부스가 생성되었습니다.")
    
    # QR 코드 URL 출력
    print("\n=== QR 코드 URL ===")
    for booth in Booth.objects.all():
        print(f"{booth.name}: http://127.0.0.1:3000/?boothId={booth.id}")

if __name__ == "__main__":
    create_sample_booths()
