import datetime
import signal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import os
import time
import _thread
import pandas as pd

from main.models import origin_files, translated_files

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def thread_translate(file,command):
    try:
        code = os.system(command)
        if code!=0:
            file.progress = 0
            file.status = 3
            file.save()
    except:
        file.progress = 0
        file.status = 3
        file.save()
def main(request):
    if request.COOKIES.get("username") is None:
        return redirect("/login")
    if request.COOKIES.get("time_start") is None:
        time_start = time.strftime("%Y-%m-%d", time.localtime())
    else:
        time_start = request.COOKIES.get("time_start")
    if request.COOKIES.get("time_end") is None:
        time_end = time.strftime("%Y-%m-%d", time.localtime(time.time()+3600*24))
    else:
        time_end = request.COOKIES.get("time_end")
    username = request.COOKIES.get("username")
    files = list()
    all_files = origin_files.objects.all().order_by('-time').filter(username__exact=username,time__gte=time_start,time__lte=time_end)
    i = 0
    for file in all_files:
        tmp = list()
        tmp.append(file.time)
        tmp.append(file.filename)
        tmp.append(file.progress)
        if file.status!=2:
            tmp.append("hidden")
        else:
            tmp.append("visible")
        fileshow = os.path.splitext(file.filename)[0][:-25]+os.path.splitext(file.filename)[1]
        if len(fileshow)>20:
            fileshow = fileshow[:17]+"..."
        tmp.append(fileshow)
        if i%2==0:
            tmp.append("#eeeeee")
        else:
            tmp.append("#dddddd")
        if file.status==3:
            tmp.append("翻译中断")
        else:
            tmp.append("")
        if file.status==1:
            tmp.append("visible")
        else:
            tmp.append("hidden")
        tmp.append(str(file.cols))
        tmp.append(str(file.completed_chars))
        print(tmp)
        files.append(tmp)
        i+=1
    context = {"username":username,"files":files,"time":[time_start,time_end]}
    return render(request, "main.html", context=context)
def upload(request):
    if request.COOKIES.get("username") is None:
        return redirect("/login")
    if request.method == "POST":
        username = request.COOKIES.get("username")
        myFile = request.FILES.get("myfile",None)
        if not myFile:
            return HttpResponse("no files for uploads")
        filename_prefix = os.path.splitext(myFile.name)[0]
        filename_suffix = os.path.splitext(myFile.name)[1]
        filename = filename_prefix + str(datetime.datetime.now())+filename_suffix
        filename = filename.replace(" ","")
        filepath = os.path.join(BASE_DIR,'files',username,'origin',filename)
        with open(filepath,'wb+') as destination:
            for chunk in myFile.chunks():
                destination.write(chunk)
        try:
            df = pd.read_csv(filepath)
        except:
            df = pd.read_excel(filepath)
        cols = df.shape[0]
        try:
            file = origin_files()
            file.filename = filename
            file.username = username
            file.status = 0
            file.progress = 0
            file.cols = cols
            file.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            file.save()
        except Exception as e:
            print(e)
            return HttpResponse("文件未上传")
        return redirect("/main")
    else:
        return HttpResponse("非法访问")

def change_time(request):
    if request.COOKIES.get("username") is None:
        return redirect("/login")
    if request.method == "POST":
        time_start = request.POST.get("time_start")
        time_end = request.POST.get("time_end")
        response = HttpResponseRedirect("/main")
        response.set_cookie("time_start",time_start,36000)
        response.set_cookie("time_end", time_end, 36000)
        return response

def translate(request):
    if request.COOKIES.get("username") is None:
        return redirect("/login")
    if request.method == "POST":
        username = request.COOKIES.get("username")
        filename = request.POST.get('filename')
        file = origin_files.objects.get(username=username, filename=filename)
        if file.status==1:
            error = "当前正在翻译"
        else:
            file.progress=0
            file.status=1
            file.save()
            exe = os.path.join(BASE_DIR,"main","google_translate.py")
            origin = os.path.join(BASE_DIR,'files',username,'origin',filename)
            target = os.path.splitext(filename)[0]+'翻译'+os.path.splitext(filename)[1]
            #log = os.path.join(BASE_DIR,'files','a.txt')
            # pid = os.fork()
            # if pid == 0:
            #     pid = os.getpid()
            #     os.system("kill -9 %s"%str(id))
            #     import pymysql
            #     conn = pymysql.connect(host="114.67.93.231", port=3306, user="ipsosuser1", password="Ipsos123456!",
            #                            database="SAAS_translation", charset="utf8")
            #     cursor = conn.cursor()
            #     sql = 'update main_origin_files set pid="%s" where filename="%s" and username="%s"'%(id,filename,username)
            #     cursor.execute(sql)
            #     conn.commit()
            #     try:
            #         tmp = os.system("python3 %s -l %s -s %s -m v2 -y win -u %s"%(exe,origin,target,username))
            #         if tmp!=0:
            #             sql = 'update main_origin_files set progress=0,status=3 where filename="%s" and username="%s"' % (
            #             filename, username)
            #             cursor.execute(sql)
            #             conn.commit()
            #     except:
            #         sql = 'update main_origin_files set progress=0,status=3 where filename="%s" and username="%s"' % (
            #             filename, username)
            #         cursor.execute(sql)
            #         conn.commit()
            command = "python3 %s -l %s -s %s -m v2 -y win -u %s"%(exe,origin,target,username)
            try:
                _thread.start_new_thread(thread_translate, (file, command,))
            except:
                file.status=3
                file.progress=0
                file.save()
        return redirect("/main")

def download(request):
    if request.method == "POST":
        filename = request.POST.get("filename")
        username = request.COOKIES.get("username")
        file = origin_files.objects.get(filename=filename,username=username)
        if file.status!=2:
            error = "还未完成无法下载"
        else:
            try:
                targetfile = [i for i in translated_files.objects.filter(origin_filename=filename,username=username)][0]
                targetfile_path = os.path.join(BASE_DIR,"files",username,"target",targetfile.target_filename)
                file = open(targetfile_path, 'rb')
                response = HttpResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="%s"'%filename
                return response
            except Exception as e:
                print(e)
                error="文件不存在"
        return redirect("/main")

def test(request):
    if request.method == "POST":
        files = request.POST.get("files").split(".$#$#$.")
        username = request.POST.get("username")
        result = list()
        for file in files:
            origin_file = origin_files.objects.get(username=username,filename=file)
            result.append(str(origin_file.progress))
    return HttpResponse(','.join(result))

def shutdown(request):
    if request.method == "POST":
        filename = request.POST.get("filename")
        username = request.COOKIES.get("username")
        print(filename,username)
        file = origin_files.objects.get(filename=filename,username=username)
        try:
            if file.pid!="-1":
                print("kill -9 %s"%file.pid)
                os.kill(int(file.pid),signal.SIGKILL)
            else:
                pass
            file.status = 0
            file.pid = -1
            file.progress = 0
            file.save()
        except Exception as e:
            file.status = 0
            file.pid = -1
            file.progress = 0
            file.save()
            print(e)
        return redirect("/main")