#!/usr/bin/env python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_create_participant():
    """참여자 생성 테스트"""
    print("=== 참여자 생성 테스트 ===")
    data = {"nickname": "춘천사는반달곰"}
    response = requests.post(f"{BASE_URL}/participants/", json=data)
    
    if response.status_code == 201:
        participant = response.json()
        print(f"✓ 참여자 생성 성공: {participant['nickname']} (ID: {participant['id']})")
        return participant['id']
    else:
        print(f"✗ 참여자 생성 실패: {response.text}")
        return None

def test_get_participant(participant_id):
    """참여자 조회 테스트"""
    print(f"\n=== 참여자 조회 테스트 ===")
    response = requests.get(f"{BASE_URL}/participants/{participant_id}/")
    
    if response.status_code == 200:
        participant = response.json()
        print(f"✓ 참여자 정보: {participant['nickname']}")
        print(f"  - 스탬프 수: {participant['stamp_count']}")
        print(f"  - 미션 완료: {participant['is_mission_complete']}")
        return True
    else:
        print(f"✗ 참여자 조회 실패: {response.text}")
        return False

def test_create_stamp(participant_id, booth_id):
    """스탬프 생성 테스트"""
    print(f"\n=== 스탬프 생성 테스트 ===")
    data = {
        "participant_id": participant_id,
        "booth_id": booth_id
    }
    response = requests.post(f"{BASE_URL}/stamps/", json=data)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✓ 스탬프 획득 성공!")
        print(f"  - 총 스탬프 수: {result['total_stamps']}")
        print(f"  - 미션 완료: {result['is_mission_complete']}")
        return True
    else:
        print(f"✗ 스탬프 생성 실패: {response.text}")
        return False

def test_admin_stats():
    """관리자 통계 테스트"""
    print(f"\n=== 관리자 통계 테스트 ===")
    response = requests.get(f"{BASE_URL}/admin/stats/")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ 통계 조회 성공:")
        print(f"  - 총 참여자 수: {stats['total_participants']}")
        print(f"  - 미션 완료자 수: {stats['total_completions']}")
        print(f"  - 부스별 인기도:")
        for booth in stats['booth_popularity'][:3]:
            print(f"    * {booth['name']}: {booth['scan_count']}회")
        return True
    else:
        print(f"✗ 통계 조회 실패: {response.text}")
        return False

if __name__ == "__main__":
    print("소양강문화제 QR 스탬프 시스템 API 테스트\n")
    
    # 샘플 부스 ID (도자기 만들기)
    booth_id = "dd010cc4-0807-4867-9039-c12ff6d4bbff"
    
    try:
        # 1. 참여자 생성
        participant_id = test_create_participant()
        if not participant_id:
            exit(1)
        
        # 2. 참여자 조회
        if not test_get_participant(participant_id):
            exit(1)
        
        # 3. 스탬프 생성
        if not test_create_stamp(participant_id, booth_id):
            exit(1)
        
        # 4. 참여자 정보 다시 조회 (스탬프 반영 확인)
        test_get_participant(participant_id)
        
        # 5. 관리자 통계 조회
        test_admin_stats()
        
        print(f"\n🎉 모든 API 테스트가 성공적으로 완료되었습니다!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Django 서버가 실행되지 않았습니다. 먼저 'python manage.py runserver'를 실행해주세요.")
