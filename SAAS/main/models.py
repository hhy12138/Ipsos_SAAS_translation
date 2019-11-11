from django.db import models

# Create your models here.
class origin_files(models.Model):
    filename = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    status = models.IntegerField()#0未在翻译，1正在翻译
    progress = models.IntegerField()
    time = models.DateTimeField()

class translated_files(models.Model):
    origin_filename = models.CharField(max_length=128)
    target_filename = models.CharField(max_length=128)
    username = models.CharField(max_length=128)

