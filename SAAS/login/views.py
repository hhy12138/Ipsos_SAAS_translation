import datetime
import random
import smtplib
from email._header_value_parser import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from login.models import password_validation


# Create your views here.
def login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            response = HttpResponseRedirect("/main")
            response.set_cookie("username",username,3600)
            return response
        else:
            error = "密码错误或用户不存在"
    return render(request,"login.html",context={"error":error})

def forgetpassword(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            email = user.email
            code = str(random.randint(1000,9999))
            valid = password_validation()
            valid.username = user.username
            valid.code = code
            valid.save()
            sender = 'ipsos_translate@126.com'
            receiver = email
            passwd = 'ipsos12345678'
            mailserver = 'smtp.126.com'
            port = '25'
            sub = 'ipsos修改密码验证码'
            msg = MIMEMultipart('related')
            msg['From'] = formataddr(["sender", sender])  # 发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["receiver", receiver])  # 收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = sub
            body = code
            text = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text)
            server = smtplib.SMTP(mailserver, port)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(sender, passwd)  # 发件人邮箱账号、邮箱密码
            server.sendmail(sender, receiver, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()
            response = HttpResponseRedirect("/login/changepassword")
            response.set_cookie("username", username, 3600)
            return response
        except Exception as e:
            print(e)
            error = "用户名不存在"
    return render(request,"forgetpassword.html",context={"error":error})
def changepassword(request):
    error = ""
    if request.method == 'POST':
        username = request.COOKIES.get("username")
        code = request.POST.get("code")
        newpassword = request.POST.get("newpassword")
        try:
            validate = password_validation.objects.filter(username__exact=username,code__exact=code).last()
            if (datetime.datetime.now()-validate.time).seconds < 900:
                user = User.objects.get(username=username)
                user.set_password(newpassword)
                user.save()
                return redirect('/login')
        except:
            error = '验证码错误'

    return render(request,"changepassword.html",context={"error":error})