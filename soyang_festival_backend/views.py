from django.http import JsonResponse
from django.shortcuts import render
from stampapp.models import Booth, Participant, Stamp

def api_root(request):
    """API 루트 엔드포인트 - 사용 가능한 API 목록을 반환"""
    api_endpoints = {
        "message": "소양강문화제 QR 스탬프 랠리 시스템 API",
        "version": "1.0",
        "endpoints": {
            "participants": {
                "create": "/api/participants/ (POST)",
                "detail": "/api/participants/{id}/ (GET)"
            },
            "stamps": {
                "create": "/api/stamps/ (POST)"
            },
            "admin": {
                "stats": "/api/admin/stats/ (GET)",
                "admin_panel": "/admin/"
            }
        },
        "sample_data": {
            "total_booths": Booth.objects.count(),
            "total_participants": Participant.objects.count(),
            "total_stamps": Stamp.objects.count()
        }
    }
    return JsonResponse(api_endpoints, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def health_check(request):
    """헬스 체크 엔드포인트"""
    return JsonResponse({
        "status": "healthy",
        "service": "soyang_festival_backend",
        "database_connected": True
    })

def favicon(request):
    """favicon.ico 요청 처리"""
    from django.http import HttpResponse
    return HttpResponse(status=204)  # No Content
