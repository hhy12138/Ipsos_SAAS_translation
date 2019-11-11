from datetime import timezone

from django.db import models

# Create your models here.
class password_validation(models.Model):
    username = models.CharField(max_length=150)
    code = models.CharField(max_length=4)
    time = models.DateTimeField(auto_now=True)