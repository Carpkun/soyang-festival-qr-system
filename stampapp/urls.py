from django.urls import path
from . import views

urlpatterns = [
    # 참여자 관련 API
    path('participants/', views.create_participant, name='create_participant'),
    path('participants/<uuid:participant_id>/', views.get_participant, name='get_participant'),
    
    # 부스 관련 API
    path('booths/', views.get_booths, name='get_booths'),
    
    # 스탬프 관련 API
    path('stamps/', views.create_stamp, name='create_stamp'),
    
    # 관리자 통계 API
    path('admin/stats/', views.admin_stats, name='admin_stats'),
]
