from rest_framework import serializers
from .models import Booth, Participant, Stamp

class BoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class ParticipantSerializer(serializers.ModelSerializer):
    stamp_count = serializers.ReadOnlyField()
    is_mission_complete = serializers.ReadOnlyField()
    
    class Meta:
        model = Participant
        fields = ['id', 'nickname', 'stamp_count', 'is_mission_complete', 'created_at']
        read_only_fields = ['id', 'created_at']

class StampSerializer(serializers.ModelSerializer):
    booth_name = serializers.CharField(source='booth.name', read_only=True)
    
    class Meta:
        model = Stamp
        fields = ['id', 'participant', 'booth', 'booth_name', 'created_at']
        read_only_fields = ['id', 'created_at']

class ParticipantDetailSerializer(ParticipantSerializer):
    stamps = StampSerializer(many=True, read_only=True)
    
    class Meta(ParticipantSerializer.Meta):
        fields = ParticipantSerializer.Meta.fields + ['stamps']
