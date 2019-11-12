from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import os

def create_account(request):
    if request.GET.get("key") == "Ipsos_translation_key":
        username = request.GET.get("username")
        password = request.GET.get("password")
        email = request.GET.get("email")
        print(username,password,email)
        if username is not None and password is not None and email is not None:
            try:
                os.system("mkdir files/%s"%username)
                os.system("mkdir files/%s/origin" % username)
                os.system("mkdir files/%s/target" % username)
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return HttpResponse("创建成功")
            except:
                return HttpResponse("创建失败")
    return HttpResponse("创建失败")