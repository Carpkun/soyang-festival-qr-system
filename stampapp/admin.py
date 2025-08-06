from django.contrib import admin
from .models import Booth, Participant, Stamp

@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'stamp_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'qr_url')
    
    def stamp_count(self, obj):
        return obj.stamps.count()
    stamp_count.short_description = '스탬프 수'

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'stamp_count', 'is_mission_complete', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nickname',)
    readonly_fields = ('id', 'created_at')
    
    def stamp_count(self, obj):
        return obj.stamp_count
    stamp_count.short_description = '스탬프 수'
    
    def is_mission_complete(self, obj):
        return obj.is_mission_complete
    is_mission_complete.short_description = '미션 완료'
    is_mission_complete.boolean = True

@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ('participant', 'booth', 'created_at')
    list_filter = ('created_at', 'booth')
    search_fields = ('participant__nickname', 'booth__name')
    readonly_fields = ('id', 'created_at')
    autocomplete_fields = ('participant', 'booth')
