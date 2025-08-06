from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Count

from .models import Booth, Participant, Stamp
from .serializers import (
    BoothSerializer, 
    ParticipantSerializer, 
    ParticipantDetailSerializer,
    StampSerializer
)

# 참여자 생성 API
@api_view(['POST'])
@permission_classes([AllowAny])
def create_participant(request):
    """
    신규 참여자 생성
    """
    serializer = ParticipantSerializer(data=request.data)
    if serializer.is_valid():
        try:
            participant = serializer.save()
            return Response(
                ParticipantSerializer(participant).data, 
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {'error': '이미 사용 중인 닉네임입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 참여자 상세 조회 API
@api_view(['GET'])
@permission_classes([AllowAny])
def get_participant(request, participant_id):
    """
    특정 참여자의 현재 스탬프 현황 조회
    """
    participant = get_object_or_404(Participant, id=participant_id)
    serializer = ParticipantDetailSerializer(participant)
    return Response(serializer.data)

# 스탬프 획득 API
@api_view(['POST'])
@permission_classes([AllowAny])
def create_stamp(request):
    """
    스탬프 획득 기록 생성
    """
    participant_id = request.data.get('participant_id')
    booth_id = request.data.get('booth_id')
    
    if not participant_id or not booth_id:
        return Response(
            {'error': 'participant_id와 booth_id가 필요합니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        participant = get_object_or_404(Participant, id=participant_id)
        booth = get_object_or_404(Booth, id=booth_id, is_active=True)
        
        # 중복 스캔 방지
        if Stamp.objects.filter(participant=participant, booth=booth).exists():
            return Response(
                {'error': '이미 스캔한 부스입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stamp = Stamp.objects.create(participant=participant, booth=booth)
        total_stamps = participant.stamps.count()
        
        return Response({
            'status': 'success',
            'total_stamps': total_stamps,
            'is_mission_complete': total_stamps >= 5
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# 부스 목록 조회 API
@api_view(['GET'])
@permission_classes([AllowAny])
def get_booths(request):
    """
    모든 활성화된 부스 목록 조회
    """
    booths = Booth.objects.filter(is_active=True).order_by('id')
    serializer = BoothSerializer(booths, many=True)
    return Response(serializer.data)

# 관리자용 통계 API
@api_view(['GET'])
@permission_classes([AllowAny])  # 실제로는 관리자 권한 필요
def admin_stats(request):
    """
    관리자 대시보드용 통계 데이터
    """
    total_participants = Participant.objects.count()
    total_completions = Participant.objects.filter(
        stamps__isnull=False
    ).annotate(
        stamp_count=Count('stamps')
    ).filter(stamp_count__gte=5).count()
    
    booth_popularity = Booth.objects.annotate(
        scan_count=Count('stamps')
    ).order_by('-scan_count').values('name', 'scan_count')[:10]
    
    return Response({
        'total_participants': total_participants,
        'total_completions': total_completions,
        'booth_popularity': list(booth_popularity)
    })
