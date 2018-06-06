import requests
from bs4 import BeautifulSoup
import pymysql
import re
import json
import threading


# header1 = del
# http://wx.233.com/tiku/exam/521-3-0-0-2
#http://wx.233.com/tiku/exam/522-3-0-0-1
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'referer':'http://wx.233.com/tiku/chapter/623',
    'Host':'wx.233.com'
}

logindata = {
    'account':'15715219240',
    'password':'a3f6acaa95e6e10a52a60858e9847b67',
    'remember': 'false'
}

class ImportThread(threading.Thread):
    def __init__(self,name,items,conn):
        threading.Thread.__init__(self)
        self.name=name
        self.items=items
        self.conn=conn
    def run(self):
        print("启动线程:"+self.name+",size:"+str(len(self.items)))
        importExamInfos(self.conn,self.items)



#登陆233网校
def login_233():
    request_session = requests.session()
    header['referer']='http://wx.233.com/tiku/exam/525-3-0-0-1'
    header['Host']='passport.233.com'
    url = "http://passport.233.com/api/singin?redirecturl='http://wx.233.com/tiku/exam/525-3-0-0-1'"
    response  = request_session.post(url,headers=header,data = logindata)
    print(response.text)
    return request_session


def exams(requests_session):
    url = "http://wx.233.com/tiku/exam/525-3-0-0-1"
    # requests_session = requests.session()
    # requests_session = requests
    header['referer'] = 'http://wx.233.com/tiku/chapter/623'
    header['Host'] = 'wx.233.com'
    k = 1
    while k <= 9:
        response  = requests_session.get(url,headers=header,data = logindata)
        # print(response.text)
        # 解析网页
        soup= BeautifulSoup(response.text,'lxml').find('div',class_='main_right clearfix').find('div',class_='pracl-dalist f-mt20 bor').find('ul')
        n = 0
        num = len(soup.find_all('li'))
        while n < num:
            chaptername = soup.find_all('li')[n].find('div').find('h3').get_text()
            zt_go = soup.find_all('li')[n].find('a',class_='zt-go').attrs['href']
            if re.findall('vip',zt_go):
                n+=1
                continue
            # href = soup.find_all('li')[n].find('div').find('h3').find_all('a')[0].attrs['href']
            chaptername = chaptername.strip()
            # 'http://wx.233.com'
            print(chaptername)
            print('http://wx.233.com'+zt_go)
            # print(href)
            id = addCategory(chaptername)
            print(id)
            # if int(id) >= 462:
            jumpTest(requests_session,'http://wx.233.com'+zt_go,id,chaptername)

            n += 1
            # if n >= 3 :
            #     return
        k+=1
        url = url[:-1]
        url = url + str(k)

def addCategory(string):
    conn = pymysql.connect(host="139.196.177.17", user="root", password="root1234", db="bst", use_unicode=True,charset="utf8")
    cur = conn.cursor()
    sql = "INSERT INTO page_category (cname,ipid,ENABLE,igrade,isubjectid,icreator,ccreator,dcreator,imodify,cmodify,dmodify) VALUES ('"+string+"',766,0,6,70,1,'admin',now(),1,'admin',now())"
    cur.execute(sql)
    conn.commit()
    cur.close()
    return cur.lastrowid
    # cur.execute("select * from page_category where cname = %s", [string])
    # repetition = cur.fetchone()
    # cur.close()
    # return repetition[0]

# 跳转到开始做题界面
def jumpTest(requests_session,testurl,id,chaptername):
    # print(requests_session)
    pagerId = testurl.split('/')[-1]
    print(pagerId)
    # if '372293' == pagerId or '372292' == pagerId:
    #     return
    url='http://wx.233.com/tiku/Paper/CheckPaperAuth?paperId='+pagerId+'&uid=24908428' # uid当前用户的userid
    header['referer']= testurl
    pagedata = {
        'paperId':pagerId,
        'uid':24908428
    }
    resp = requests_session.get(url,headers=header,data = pagedata)
    print(resp.text)
    resp = json.loads(resp.text)
    print(resp['list'][0]['url'])
    url = resp['list'][0]['url']
    # 已经加密过md5，可以直接跳转
    doExam(requests_session,url,id,chaptername)
    # bs = BeautifulSoup(resp.text,'lxml').find("a",class_='test mokao').attrs['href']
    # resp = requests_session.get(bs,headers=header)
    # print(resp.status_code)

# 题目开始考试页面
def doExam(requests_session,doexamUrl,id,chaptername):
    res = requests_session.get(doexamUrl, headers=header)
    # print(res.text)
    if re.findall(r'extractExam',doexamUrl):
        url = 'http://wx.233.com/tiku/api/exam/'
        dataex = {'url':'eyJDbGFzc0lkIjo1MjEsIlR5cGUiOjEsIk9iamVjdElkIjozNjIyNDgsIkV4YW1UeXBlIjpudWxsLCJFeHRyYWN0VHlwZSI6MCwiTW9kZSI6MiwiUmVkbyI6ZmFsc2UsIklzQ29udGludWUiOmZhbHNlLCJDb3VudCI6MCwiUGFnZUluZGV4IjowLCJQYWdlU2l6ZSI6MCwiSXNBdXRvRGVsUmlnaHQiOjAsIkZyb21VcmwiOiJodHRwOi8vd3guMjMzLmNvbS90aWt1L2V4YW0/Y2xhc3NJZD01MjEiLCJSYW5rIjowfQ=='}
        res = requests_session.post(url, headers=header,data = dataex)
        directurljson = json.loads(res.text)
        print('http://wx.233.com'+directurljson['list']['url'])
        directurl = 'http://wx.233.com'+directurljson['list']['url']
        doExam(requests_session, directurl, id, chaptername)
        print(res.text)
    elif re.findall('md5', doexamUrl):
        string = re.findall(r'md5=\S*&', doexamUrl)
        md5str = string[0].split('&')[0]
        # print(md5str)
        getCardUrl = 'http://wx.233.com/tiku/exam/getCard?'+md5str+'&isShowExamType=1&isShowRw=1&isError=0&_=1528094083351'
        # getCardUrl = int(getCardUrl.split('=')[-1])+4
        res = requests_session.get(getCardUrl,headers=header)
        result = json.loads(res.text)
        ruleIds = result['list']
        for item in ruleIds:
            ruleIds = str(item["examRule"])
            getExamUrl = 'http://wx.233.com/tiku/exam/GetExam?'+md5str+'&type=1&ruleId='+ruleIds+'&pageIndex=1&pageSize=1000&_=1528093162870'
            questions  = requests_session.get(getExamUrl,headers=header)
            print(questions.text)
            importJsonDate(questions.text,id,chaptername)
    else:
        urlstr = doexamUrl.split('?')[0]
        md5str = urlstr.split('/')[-1]
        getCardUrl = 'http://wx.233.com/tiku/exam/getCard?md5='+md5str+'&isShowExamType=1&isShowRw=1&isError=0&_=1528094083351'
        res = requests_session.get(getCardUrl, headers=header)
        result = json.loads(res.text)
        # print(result)
        ruleIdst = result['list']
        for item in ruleIdst:
            ruleIdstr = str(item["examRule"])
            getExamUrl = 'http://wx.233.com/tiku/exam/GetExam?md5=' + md5str + '&type=1&ruleId=' + ruleIdstr + '&pageIndex=1&pageSize=1000&_=1528093162870'
            questions = requests_session.get(getExamUrl, headers=header)
            print(questions.text)
            importJsonDate(questions.text,id,chaptername)

##读取json 整理成相应格式
def importJsonDate(questionlist,id,chaptername):
    #读取本地json 文件，获取所有的文件信息
    # filepath= r'C:\Users\Administrator\Desktop\test\questions.json'
    # category = " 2013年中级社会工作者考试《社会工作实务》真题及解析 ".strip()
    category = chaptername.strip()
    icategory = id
    result = []
    # with open(filepath,"r",encoding="utf-8") as filecontent:
    #     # json.dump(data,filecontent)
    #     content = filecontent.read()
    review_text = json.loads(questionlist) # 解析数据
    # print(review_text["list"]["examDtoList"])
    examsQuestions = review_text["list"]["examDtoList"]
    n = 0
    while n < len(examsQuestions):
        jxcontent =examsQuestions[n]["analysis"]
        answer = examsQuestions[n]["answer"]
        title = examsQuestions[n]['content']
        answerArr = examsQuestions[n]['optionList']
        orderid = examsQuestions[n]['orderId']

        type = examsQuestions[n]["examType"]
        ctype = examsQuestions[n]["examTypeName"]

        qanswers = []
        if 1 == type:
            type = 0 # 0 为单选题
            #答案整理成固定格式
            qanswers = answers(answerArr, answer)
        elif 2 == type:
            type = 1 # 1为多选题
            qanswers = answers(answerArr, answer)
        elif 3 == type:
            type = 2  # 2为判断题
        elif 7 == type or re.match(r"简答",ctype):
            type = 3  # 3为简答题

        result.append({"type":type,"qyname":title,"qanswers":qanswers,"qcontent":jxcontent,"titleImg":"","jxImg":"","category":category,"icategory":icategory,"orderid":orderid})
        n+=1
    print(len(result))
    print(result)
    threadImportInfo(result, 50)
    return result

def answers(qanswer,ans):
    arr = qanswer
    if ans == '无正确答案':
        ans = "H"
    # ans = "B,C"
    repl = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
    if re.findall(r'，',ans):
        ans = re.sub(r"，",',',ans)
    anss = re.split(r",",ans)
    qanswers = []
    i = 0
    for item in arr:
        i += 1
        qq = {"iscorrect":1,"label":item,"img":"","index":i}
        for a in anss:
            if i == repl[a]:
                qq["iscorrect"] = 0
        qanswers.append(qq)
    # print(qanswers)
    return qanswers

def importExamInfos(conn,items):
    # icategory = addCategory(conn, items)
    for item in items:
        importDB(conn,item)

def importDB(conn,item):
    questionId = addQuestion(conn,item)
    if None == item['qanswers'] or len(item['qanswers'])==0 or item['type'] ==3: #简答题没有答案要插入
        return
    addAnswer(conn,item["qanswers"],questionId)

def threadImportInfo(items,listSize=20):
    examSize = len(items)
    if listSize <= 0 :
        listSize = 20

    if listSize >= examSize :
        listSize = examSize

    threadSize = examSize//listSize
    yushu = examSize%listSize

    if yushu != 0 :
        threadSize = threadSize+1

    conn = pymysql.connect(host="139.196.177.17",user="root",password="root1234",db="bst",use_unicode=True,charset="utf8")
    # icategory = addCategory(conn,items)
    # icategory = 426
    # print(icategory)
    #创建线程
    threadLock = threading.Lock()
    threads = []
    for i in range(1,threadSize+1):
        conn = pymysql.connect(host="139.196.177.17",user="root",password="root1234",db="bst",use_unicode=True,charset="utf8")
        threadItem = ImportThread("ImportThread:"+str(i),items[(i-1)*listSize:i*listSize],conn)
        threadItem.start()
        threads.append(threadItem)

    # 等待所有线程完成
    for t in threads:
        t.join()

#添加题目,并返回题目的id
def addQuestion(conn,item):
    print(item)
    title = item["qyname"]
    jx=item["qcontent"]
    titleImg=item["titleImg"]
    jxImg=item["jxImg"]
    qtype=item["type"]
    ichapterid=item["icategory"]
    cchaptername=item["category"]

    cur = conn.cursor()
    cur.executemany("insert into page_question (ctitle, ccontent, ctype, titleimage, contentimage, page_category_id, icreator, ccreator, dcreator, imodify, cmodify, dmodify, isort, ichapterid, cchaptername, cremark, onelevel, twolevel) VALUES (%s, %s, %s, %s, %s, 70, 20, 'admin', now(), 20, 'admin', now(), 0, %s, %s, 'python', 65, 66)",[(title,jx,qtype,titleImg,jxImg,ichapterid,cchaptername)])
    conn.commit()
    cur.close()
    #获取自增id
    return cur.lastrowid

def addAnswer(conn,answerItems,questionId):
    cur = conn.cursor()
    # index=0 #排序
    for item in answerItems :
        sql="insert into page_answer (iscorrect, ccontent, ctype, icreator, ccreator, dcreator, imodify, cmodify, dmodify, imageurl, page_question_id, isort) VALUES ("+str(item["iscorrect"])+", '"+item["label"]+"', '0', 20, 'admin', now(), 20, 'admin', now(), '"+item["img"]+"', "+str(questionId)+","+str(item["index"])+")"
        cur.execute(sql)
        conn.commit()
        # index=index+1
    cur.close()

if __name__=='__main__':
    request_session = login_233()
    exams(request_session)
    # exams = importJsonDate()
    # threadImportInfo(exams, 50)
    # exams(None)