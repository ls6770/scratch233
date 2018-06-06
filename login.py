import requests
from bs4 import BeautifulSoup
import json
#模拟登陆的爬虫
login_session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'Host': 'passport.233.com',
    'referer':'http://passport.233.com/login'
}
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'referer':'http://passport.233.com/login'
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'referer':'http://wx.233.com/tiku/chapter/623'
}
postdata = {
    'account':'15715219240',
    'password':'a3f6acaa95e6e10a52a60858e9847b67',
    'remember': 'false'
}

login_url = "http://passport.233.com/api/singin?redirectUrl='http://wx.233.com/uc'"
#用户登陆方法
result = login_session.post(login_url,headers=headers,data=postdata)
print(result.text)
result = login_session.get("http://wx.233.com/uc",headers=headers1)
result = login_session.get("http://wx.233.com/tiku/chapter/623",headers=headers2)

#跳转到的做题的 chapterId章节id，从页面上获取
# url = "http://wx.233.com/tiku/exam/extractexam?classId=521&type=2&mode=1&objectid=" + chapterId +
# "&examtype=-1&count=0&redo=false&isContinue=true&isNotLogin=1&fromUrl=http://wx.233.com/tiku/chapter/623;
url1 = "http://wx.233.com/tiku/exam/extractexam?classId=521&type=2&mode=1&objectid=55794&examtype=-1&count=0&redo=false&isContinue=true&isNotLogin=1&fromUrl=http://wx.233.com/tiku/chapter/623"
result = login_session.get("http://wx.233.com/tiku/exam/extractexam?classId=521&type=2&mode=1&objectid=55794&examtype=-1&count=0&redo=false&isContinue=true&isNotLogin=1&fromUrl=http://wx.233.com/tiku/chapter/623&extractType=0",headers=headers2)

data = { 'url': 'eyJDbGFzc0lkIjo1MjEsIlR5cGUiOjIsIk9iamVjdElkIjo1NTc5NCwiRXhhbVR5cGUiOiItMSIsIkV4dHJhY3RUeXBlIjowLCJNb2RlIjoxLCJSZWRvIjpmYWxzZSwiSXNDb250aW51ZSI6dHJ1ZSwiQ291bnQiOjAsIlBhZ2VJbmRleCI6MCwiUGFnZVNpemUiOjAsIklzQXV0b0RlbFJpZ2h0IjowLCJGcm9tVXJsIjoiaHR0cDovL3d4LjIzMy5jb20vdGlrdS9jaGFwdGVyLzYyMyIsIlJhbmsiOjB9' }
url = "http://wx.233.com/tiku/api/exam/"
headers2['referer']=url1
headers2['Host'] ='wx.233.com'
result = login_session.post(url,headers=headers2,data=data)
result = eval(result.text)
print(result)
result = login_session.get('http://wx.233.com'+result['list']['url'],headers=headers2)
print(result.text)
print(result.cookies)
result.status_code # 200请求成功