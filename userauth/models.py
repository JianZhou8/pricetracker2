from django.db import models
from django.contrib.auth.models import User

class TrackList(models.Model):
    user = models.ForeignKey(User, default=1,  on_delete=models.CASCADE)  # 添加用户外键
    number = models.IntegerField()
    url = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    check_frequency = models.IntegerField(default=10)
    last_check_time = models.DateTimeField(auto_now_add=True)
    enable_auto_monitoring = models.BooleanField(default=False)
    timer_id = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"TrackList {self.number}"

