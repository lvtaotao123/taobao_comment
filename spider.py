import requests,time,json
import xlwt,re,random

session = requests.session()
headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host':'s.taobao.com'
        }

with open('cookie.txt', 'r') as f:  
        cookie = f.read()
        cookieDict = {}
        cookies = cookie.split("; ")
        for co in cookies:
            co = co.strip()
            p = co.split('=')
            cookieDict[p[0]] = p[1] 
session.cookies.update(cookieDict)

def spider(itemid,userid):
    global filename,testdata
    page,row = 1,1
    wb = xlwt.Workbook()
    ws = wb.add_sheet('评论')
    ws.write(0,0,'用户')
    ws.write(0,1,'评论内容')
    while True:
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&order=3&currentPage={}&append=0&\
content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hv%2BpvLvZUvUvCkvvvvvjiPRLMptjrnRFdyAj3mPmPOsjtEPscOsjYURsSWgjEv9phvHHiavU92zHi4\
70d%2BtM1D7M14NrGBdphvmpvUtvSDtp2MKu6Cvvyvm8Qb9UvvTlurvpvEvv9umTKdvnGnRphvCvvvvvmjvpvhvvpvv8wCvvpvvUmmRphvCvvvvvmEvpvVmvvC9jXPuphvmvv\
v9bLs%2BX7AKphv8vvvvvCvpCBXvvvCzhCv2j9vvUEpphvWh9vv9DCvpvQovvmmZhCv2CUEvpCWCj11vvaAQWFhsmTTwhbWecjxVCDAo5jxQW94V31iQWFh0mTTwhbvzjjxVC\
D1pjjxQWkX%2BC1iQWFWDoTTwhbptjjxVCD6BzjxQWkOWphCvvOvCvvvphvPvpvhvv2MMT6CvvyvCEO8AG%2BvI18CvpvW7DdikEsw7Di4B1dNdphvmpvUo9Set92bAu6Cvvyv\
2vWbvphhW8wtvpvhvvvvvv%3D%3D&needFold=0&_ksTS={}_2699&callback=jsonp2700'.format(itemid,userid,page,int(round(time.time()*1000)))
        try:
            text = session.get(url,headers=headers).text
            text = text.split('(',1)[1]
            text = text[:len(text)-1]
            js = json.loads(text)
            testdata = js
            if not len(js['rateDetail']['rateList']):
                print('已完成第{}个货品评论爬取'.format(filename))
                wb.save('U盘'+str(filename)+'.xls')
                filename += 1
                break
        except:
            print('已完成第{}个货品评论爬取'.format(filename))
            wb.save('U盘'+str(filename)+'.xls')
            filename += 1
            break
        for i in range(len(js['rateDetail']['rateList'])):
            #用户名
            name = js['rateDetail']['rateList'][i]['displayUserNick']
            #评论
            comment = js['rateDetail']['rateList'][i]['rateContent']
            with open('U盘'+str(filename)+'.txt','a',errors = 'ignore') as f:
                f.write(name+'   '+comment+'\n')
            ws.write(row,0,name)
            ws.write(row,1,comment)
            row+=1
        if page == 21:
            print('已完成第{}个货品评论爬取'.format(filename))
            wb.save('U盘'+str(filename)+'.xls')
            filename += 1
            break
        print('评论当前页数:',page)
        time.sleep(random.randint(10,15))
        page += 1

if __name__=='__main__':
    filename = 1
    testdata = ''
    #从主页提取seller和itemid
    main_url = 'https://s.taobao.com/search?spm=a230r.1.1998181369.d4919860.1bc14a0ey1okwq&q=U%E7%9B%98&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&ie=utf8&initiative_id=tbindexz_20170306&tab=mall'
    text = session.get(main_url,headers=headers).text
    userIds = re.findall('"user_id":(.*?),"nick"',text)
    itemIds = re.findall('"allNids":\[(.*?)\]',text)[0].split(',')
    headers['Host'] = 'rate.tmall.com'
    print(len(userIds),len(itemIds))
    for i in range(0,22):
        itemid = itemIds[i].strip('"')
        userid = userIds[i].strip('"')
        with open('U盘'+str(filename)+'.txt','a',errors = 'ignore') as f:
            url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hv%2BpvLvZUvUvCkvvvvvjiPRLMptjrnRFdyAj3mPmPOsjtEPscOsjYURsSWgjEv9phvHHiavU92zHi470d%2BtM1D7M14NrGBdphvmpvUtvSDtp2MKu6Cvvyvm8Qb9UvvTlurvpvEvv9umTKdvnGnRphvCvvvvvmjvpvhvvpvv8wCvvpvvUmmRphvCvvvvvmEvpvVmvvC9jXPuphvmvvv9bLs%2BX7AKphv8vvvvvCvpCBXvvvCzhCv2j9vvUEpphvWh9vv9DCvpvQovvmmZhCv2CUEvpCWCj11vvaAQWFhsmTTwhbWecjxVCDAo5jxQW94V31iQWFh0mTTwhbvzjjxVCD1pjjxQWkX%2BC1iQWFWDoTTwhbptjjxVCD6BzjxQWkOWphCvvOvCvvvphvPvpvhvv2MMT6CvvyvCEO8AG%2BvI18CvpvW7DdikEsw7Di4B1dNdphvmpvUo9Set92bAu6Cvvyv2vWbvphhW8wtvpvhvvvvvv%3D%3D&needFold=0&_ksTS={}_2699&callback=jsonp2700'.format(itemid,userid,1,int(round(time.time()*1000)))
            f.write(url+'\n')
        spider(itemid,userid)
        
        
    

    
