import json
import re
import threading
import pymysql

class ImportThread(threading.Thread):
    def __init__(self,name,items,conn,icategory):
        threading.Thread.__init__(self)
        self.name=name
        self.items=items
        self.conn=conn
        self.icategory=icategory
    def run(self):
        print("启动线程:"+self.name+",size:"+str(len(self.items)))
        importExamInfos(self.conn,self.items,self.icategory)

def importJsonDate():
    #读取本地json 文件，获取所有的文件信息
    filepath= r'C:\Users\Administrator\Desktop\test\questions.json'
    category = " 2013年中级社会工作者考试《社会工作实务》真题及解析 ".strip()
    icategory = ""
    result = []
    # filecontent = open(filepath,encoding="utf8")
    with open(filepath,"r",encoding="utf-8") as filecontent:
        # json.dump(data,filecontent)
        content = filecontent.read()
        review_text = json.loads(content) # 解析数据
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

def threadImportInfo(items,listSize=20):
    examSize = len(exams)
    if listSize <= 0 :
        listSize = 20

    if listSize >= examSize :
        listSize = examSize

    threadSize = examSize//listSize
    yushu = examSize%listSize

    if yushu != 0 :
        threadSize = threadSize+1

    conn = pymysql.connect(host="139.196.177.17",user="root",password="root1234",db="bst",use_unicode=True,charset="utf8")
    icategory = addCategory(conn,items)
    # icategory = 426
    print(icategory)
    #创建线程
    threadLock = threading.Lock()
    threads = []
    for i in range(1,threadSize+1):
        conn = pymysql.connect(host="139.196.177.17",user="root",password="root1234",db="bst",use_unicode=True,charset="utf8")
        threadItem = ImportThread("ImportThread:"+str(i),items[(i-1)*listSize:i*listSize],conn,icategory)
        threadItem.start()
        threads.append(threadItem)

    # 等待所有线程完成
    for t in threads:
        t.join()

def addCategory(conn,items):
    cur = conn.cursor()
    sql = "INSERT INTO page_category (cname,ipid,ENABLE,igrade,isubjectid,icreator,ccreator,dcreator,imodify,cmodify,dmodify) VALUES ('"+str(items[0]['category'])+"',421,0,5,70,1,'admin',now(),1,'admin',now())"
    cur.execute(sql)
    conn.commit()
    cur.close()
    return cur.lastrowid

def importExamInfos(conn,items,icategory):
    for item in items:
        item['icategory'] = icategory
        importDB(conn,item)

def importDB(conn,item):
    # pagerId = addPager(conn,item)
    # questions = readExamQuestionInfo(item["sjname"])
    # print("试卷:"+item["sjname"])
    # for question in item:
    questionId = addQuestion(conn,item)
    #addExamQuextion(conn,pagerId,questionId,question["qtype"],question["xh"])
    if None == item['qanswers'] or len(item['qanswers'])==0 or item['type'] ==3: #简答题没有答案要插入
        return
    addAnswer(conn,item["qanswers"],questionId)

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
    orderid = item["orderid"]

    cur = conn.cursor()
    cur.executemany("insert into page_question (ctitle, ccontent, ctype, titleimage, contentimage, page_category_id, icreator, ccreator, dcreator, imodify, cmodify, dmodify, isort, ichapterid, cchaptername, cremark, onelevel, twolevel) VALUES (%s, %s, %s, %s, %s, 70, 20, 'admin', now(), 20, 'admin', now(), %s, %s, %s, 'python', 65, 66)",[(title,jx,qtype,titleImg,jxImg,orderid,ichapterid,cchaptername)])
    conn.commit()
    cur.close()
    #获取自增id
    return cur.lastrowid

#添加试卷与题目的关联
def addExamQuextion(conn,ipagerid,iquestionid,iquestiontype,isort):
    cur = conn.cursor()
    cur.executemany("INSERT INTO page_pager_question (ipagerid, iquestionid, iquestiontype, isort, iversion, iscore) VALUES (%s, %s, %s, %s, 0, 0)",[(ipagerid,iquestionid,iquestiontype,isort)])
    conn.commit()
    cur.close()

def addAnswer(conn,answerItems,questionId):
    cur = conn.cursor()
    # index=0 #排序
    for item in answerItems :
        sql="insert into page_answer (iscorrect, ccontent, ctype, icreator, ccreator, dcreator, imodify, cmodify, dmodify, imageurl, page_question_id, isort) VALUES ("+str(item["iscorrect"])+", '"+item["label"]+"', '0', 20, 'admin', now(), 20, 'admin', now(), '"+item["img"]+"', "+str(questionId)+","+str(item["index"])+")"
        cur.execute(sql)
        conn.commit()
        # index=index+1
    cur.close()


if __name__ == '__main__':
    exams = importJsonDate()
    threadImportInfo(exams, 50)