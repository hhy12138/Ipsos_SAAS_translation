from django.db import models

# Create your models here.
class origin_files(models.Model):
    filename = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    status = models.IntegerField()#0未在翻译，1正在翻译
    progress = models.IntegerField()
    time = models.DateTimeField()
    pid = models.CharField(max_length=10,default=-1)
    cols = models.IntegerField(default=0)
    completed_chars = models.IntegerField(default=0)

class translated_files(models.Model):
    origin_filename = models.CharField(max_length=128)
    target_filename = models.CharField(max_length=128)
    username = models.CharField(max_length=128)

class translate_queue(models.Model):
    filename = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now=True)

class translated_chars(models.Model):
    time = models.DateTimeField(auto_now=True)
    char_num = models.IntegerField()

