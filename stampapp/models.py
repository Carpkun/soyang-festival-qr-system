from django.db import models
import uuid

# Booth information
class Booth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="부스 이름")
    description = models.TextField(max_length=500, blank=True, verbose_name="부스 설명")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시각")

    class Meta:
        verbose_name = "체험 부스"
        verbose_name_plural = "체험 부스들"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def qr_url(self):
        return f"https://ccculture.pythonanywhere.com/?boothId={self.id}"

# Participant information
class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, unique=True, verbose_name="닉네임")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시각")

    class Meta:
        verbose_name = "참여자"
        verbose_name_plural = "참여자들"
        ordering = ['-created_at']

    def __str__(self):
        return self.nickname

    @property
    def stamp_count(self):
        return self.stamps.count()

    @property
    def is_mission_complete(self):
        return self.stamp_count >= 5

# Stamp record
class Stamp(models.Model):
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='stamps')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='stamps')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="획득 시각")

    class Meta:
        verbose_name = "스탬프 기록"
        verbose_name_plural = "스탬프 기록들"
        unique_together = ("participant", "booth")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.participant.nickname} - {self.booth.name}"
