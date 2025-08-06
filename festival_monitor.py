#!/usr/bin/env python3
"""
축제 현장 실시간 모니터링 스크립트
PythonAnywhere Hacker 플랜에서 실행
"""

import os
import django
import time
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soyang_festival_backend.settings_mysql')
django.setup()

from stampapp.models import Participant, Stamp, Booth

def get_current_stats():
    """현재 시점 통계 조회"""
    now = datetime.now()
    today = now.date()
    
    # 오늘 통계
    participants_today = Participant.objects.filter(created_at__date=today).count()
    stamps_today = Stamp.objects.filter(created_at__date=today).count()
    
    # 최근 1시간 통계
    one_hour_ago = now - timedelta(hours=1)
    participants_hour = Participant.objects.filter(created_at__gte=one_hour_ago).count()
    stamps_hour = Stamp.objects.filter(created_at__gte=one_hour_ago).count()
    
    # 최근 10분 통계 (실시간 부하 측정)
    ten_min_ago = now - timedelta(minutes=10)
    participants_10min = Participant.objects.filter(created_at__gte=ten_min_ago).count()
    stamps_10min = Stamp.objects.filter(created_at__gte=ten_min_ago).count()
    
    return {
        'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
        'today': {
            'participants': participants_today,
            'stamps': stamps_today,
        },
        'last_hour': {
            'participants': participants_hour,
            'stamps': stamps_hour,
        },
        'last_10min': {
            'participants': participants_10min,
            'stamps': stamps_10min,
            'load_level': get_load_level(stamps_10min)
        }
    }

def get_load_level(stamps_10min):
    """부하 수준 판단"""
    if stamps_10min >= 50:
        return "🔴 HIGH (CPU 주의)"
    elif stamps_10min >= 20:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"

def print_stats():
    """통계 출력"""
    stats = get_current_stats()
    
    print(f"\n{'='*50}")
    print(f"🎪 소양강문화제 QR 시스템 모니터링")
    print(f"{'='*50}")
    print(f"⏰ 시간: {stats['timestamp']}")
    print(f"\n📊 오늘 누적:")
    print(f"   👥 참여자: {stats['today']['participants']}명")
    print(f"   📱 스탬프: {stats['today']['stamps']}개")
    
    print(f"\n⚡ 최근 1시간:")
    print(f"   👥 신규 참여자: {stats['last_hour']['participants']}명")
    print(f"   📱 스탬프 스캔: {stats['last_hour']['stamps']}개")
    
    print(f"\n🚨 실시간 부하 (최근 10분):")
    print(f"   👥 신규 참여자: {stats['last_10min']['participants']}명")
    print(f"   📱 스탬프 스캔: {stats['last_10min']['stamps']}개")
    print(f"   📈 부하 수준: {stats['last_10min']['load_level']}")
    
    # 경고 메시지
    if stats['last_10min']['stamps'] >= 50:
        print(f"\n⚠️  경고: 높은 부하가 감지되었습니다!")
        print(f"   - CPU 사용량을 모니터링하세요")
        print(f"   - 관리자 작업을 최소화하세요")
    
    print(f"{'='*50}")

def monitor_loop():
    """모니터링 루프"""
    print("🎪 축제 현장 모니터링 시작...")
    print("Ctrl+C로 종료")
    
    try:
        while True:
            print_stats()
            time.sleep(60)  # 1분마다 갱신
    except KeyboardInterrupt:
        print("\n👋 모니터링 종료")

if __name__ == "__main__":
    # 단발성 실행
    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--once':
        print_stats()
    else:
        # 지속적 모니터링
        monitor_loop()
