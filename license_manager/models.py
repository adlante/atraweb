from django.db import models


class HardwareLicense(models.Model):
    device_id = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.device_id} - Active: {self.is_active}"
