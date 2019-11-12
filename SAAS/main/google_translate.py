#!/usr/bin/env python
# coding: utf-8

# In[30]:


# coding: utf-8
import os
from math import floor

import pymysql
# os.system('pip install argparse')
import argparse
import re
import threading

try:
    import requests
    import pandas as pd
    from tqdm import tqdm,tqdm_notebook
    import emoji
    import openpyxl

except:
    os.system('pip install openpyxl')
    os.system('pip install requests')
    os.system('pip install pandas')
    os.system('pip install tqdm')
    os.system('pip install emoji')
    import openpyxl
    import requests
    import pandas as pd
    from tqdm import tqdm,tqdm_notebook
    import emoji
completed = 0
completed_chars = 0
def google_tran(df,model,syst,filename,username):
    if model!='v2':
        try:
            from google.cloud import translate_v3beta1 as translate
        except:
            os.system('pip install google-cloud-translate')
            from google.cloud import translate_v3beta1 as translate
    # df=pd.read_csv('export_mentions_200336_335807_2019-08-14T05_28_14.csv').astype('str')
    

    def eliminate_emojis(word):
        return ''.join(c for c in word if c not in emoji.UNICODE_EMOJI)

    def tran(content):
        # language_type = "de"
        url = "https://translation.googleapis.com/language/translate/v2"
        data = {
            'key': 'AIzaSyBZa_oeKPGR2hlt2BYjm4t8-q85UeIRV1o',
            # 'source': language_type,
            'target': 'zh_cn',
            'q': content,
            'format': 'text'
        }
        headers = {'X-HTTP-Method-Override': 'GET'}
        response = requests.post(url, data=data, headers=headers)
        res = response.json()
        text = res["data"]["translations"][0]["translatedText"]
        return text
    def tran_v3(content,model,syst):
        # model = model[2:]
        if model == 'pbmt':
            model = 'base'
        else:
            model='nmt'
        basepath = os.path.abspath('.')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(basepath,'Ipsos-translation-c094ada851a7.json')
        client = translate.TranslationServiceClient()

        project_id = "ipsos-translation"

        location = 'global'

        parent = client.location_path(project_id, location)
        response = client.translate_text(
            parent=parent,
            contents=[content],
            mime_type='text/plain',  # mime types: text/plain, text/html
            model='projects/ipsos-translation/locations/global/models/general/%s'%model,
            source_language_code='en-US',
            target_language_code='zh-CN')
        result = response.translations[0].translated_text
        return result

    trancontent = []
    global completed
    global completed_chars
    count = df.shape[0]*3
    for i, content in enumerate(tqdm(df['Mention Title'].astype('str'))):
        # print(content)
        completed_chars+=len(content)
        if len(content) > 15000:
            content = content[:15000]
        try:
            if model=='v2':
                text = tran(eliminate_emojis(content))
            elif model[:2]=='v3':
                text = tran_v3(eliminate_emojis(content),model,syst)
        except Exception as e:
            print(e)
            try:
                if model == 'v2':
                    text = tran(eliminate_emojis(content))
                elif model[:2] == 'v3':
                    text = tran_v3(eliminate_emojis(content), model, syst)
            except:
                try:
                    if model == 'v2':
                        text = tran(eliminate_emojis(content))
                    elif model[:2] == 'v3':
                        text = tran_v3(eliminate_emojis(content), model, syst)
                except:
                    text = '翻译失败'
        trancontent.append(text)
        completed+=1
        progress = min(floor(completed/count*100),99)
        if progress%5==0:
            try:
                sql = 'update main_origin_files set progress=%s,completed_chars=%s where username="%s" and filename="%s"'%(str(progress),str(completed_chars),username,filename)
                print(sql)
                conn = pymysql.connect(host="localhost", port=3306, user="ipsosuser1", password="Ipsos123456!", database="SAAS_translation",
                                       charset="utf8")
                cursor  = conn.cursor()
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)

    df['_translated'] = trancontent
    #df.to_excel(savefile)
    return df


# In[31]:


class MyThread(threading.Thread):
    completed = 0
    def __init__(self,target,args=()):
        super(MyThread,self).__init__()
        self.target = target
        self.args = args
    
    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


# In[51]:



if __name__=='__main__':
    pymysql.install_as_MySQLdb()
    conn = pymysql.connect(host="localhost",port=3306,user ="ipsosuser1", password ="Ipsos123456!",database ="SAAS_translation",charset ="utf8")
    cursor = conn.cursor()
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--loadfile',dest = "load", help = "pleaer enter the loadfile")
    parser.add_argument('-s','--savefile',dest = "save", help = "pleaer enter the savefile")
    parser.add_argument('-m', '--model', dest="model", help="pleaer enter the savefile")
    parser.add_argument('-y', '--system', dest="syst", help="pleaer enter the savefile")
    parser.add_argument('-u', '--username', dest="username", help="pleaer enter the savefile")
    args = parser.parse_args()
    print(r'----------------')
    print(r'----------------')
    print(r'----------------')
    print(r'输入格式为python python文件路径 -load 要读取的文件路径（csv后缀） -save 要保存的文件路径（xlsx后缀)')
    print(r'输入的是完整的不含中文的英文路径，不包含空格和横杠，如D:\Translate.xlsx')
    print(r'完整例子如： python D:\google_translate_1031.py -load D:\thefileloaded.csv -save D:\thefilesaved.xlsx')
    print(r'读取的时候是csv文件保存的时候是excel文件.也可以直接打开源码修改第65行')
    print(r'----------------')
    print(r'----------------')
    print(r'----------------')
    if (args.load[-3:]!='csv')and(args.load[-4:]!='xlsx') :
        raise("读取文件路径有误")
    if  args.save[-4:]!='xlsx':
        raise ("保存文件路径有误")
    if args.model is None:
        args.model = 'v3nmt'
    if args.syst is None:
        args.syst = 'win'
    t_data=[]
    origin = os.path.basename(args.load)
    target = os.path.basename(args.save)
    username = args.username
    pid = os.getpid()
    print(pid)
    sql = 'update main_origin_files set pid="%s" where filename="%s" and username="%s"'%(pid,origin,username)
    cursor.execute(sql)
    conn.commit()
    #loadfile=r'C:\Users\hehao\google translate\test.xlsx'
    #model='v2'
    #syst='win'
    print('正在读取')
    if args.load[-3:]=='csv':
        df=pd.read_csv(args.load).astype('str')
    else:
        df=pd.read_excel(args.load).astype('str')
    df = df[['true_country','Date','Time', 'Mention Title']]
    count=int(df.shape[0]/3)
    t_list=[]
    t_data=[]
    t1=MyThread(target=google_tran,args=(df[0:count],args.model,args.syst,origin,username))
    t2=MyThread(target=google_tran,args=(df[count:count*2],args.model,args.syst,origin,username))
    t3=MyThread(target=google_tran,args=(df[count*2:],args.model,args.syst,origin,username))
    for t in [t1,t2,t3]:
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()
        t_data.append(t.get_result())
    df_opt=pd.concat(t_data)
    path = os.path.join(os.path.realpath(".."),'files',username,'target',args.save)
    print(path,args.save,1)
    df_opt.to_excel(os.path.join(os.path.realpath("."),'files',username,'target',args.save))
    print('翻译结束')
    try:
        sql = 'update main_origin_files set progress=100,status=2 where filename="%s" and username="%s"'%(origin,username)
        print(sql)
        cursor.execute(sql)
        sql = 'insert main_translated_files values(null,"%s","%s","%s")' % (origin,target,username)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)


# In[ ]:




