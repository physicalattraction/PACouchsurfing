from django.db import models


class Profile(models.Model):
    public_name = models.CharField(max_length=64)
    public_address = models.CharField(max_length=256, blank=True, default='')
    avatar_url = models.URLField(null=True, blank=True, default='')
    is_verified = models.BooleanField()
    is_deleted = models.BooleanField()
