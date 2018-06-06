import json
import re
import urlparse3
import pymysql

# result = "{'list':{'url':'http'}}"
# result = eval(result)
# print(result['list']['url'])


# if re.match(r"\S*单选","[单选]"):
#     print(True)
# else:
#     print(False)
def answers(qanswer,ans):
    str = qanswer
    repl = ("A","B","C","D","E","F","G","H")
    # ans = "B,C"
    anss = re.split(r",",ans)
    qanswers = []
    for item in repl:
        str = re.sub(r""+item+".",item+"."+"1",str)
    print(str)
    for key in anss:
        print(key)
        str = re.sub(r""+key+".1",key+"."+"0",str)
        print(str)

    answers = re.split(r"[A-H].",str.strip())
    print(len(answers))
    index = 1
    for answer in answers:
        if len(answer) != 0:
            answer = re.findall(r"^\S*",answer.strip())
            #print(answer[0])
            answer1 = answer[0][0]
            #print(answer1)
            if answer1 == 0:
                answer1 = answer[0][1,].strip()
            else:
                answer1 = answer[0].strip()
            print(answer1[0:1],answer1[1:])
            qanswers.append({"iscorrect":answer1[0:1],"label":answer1[1:],"img":"","index":index})
            index +=1
    return qanswers

def method():
    str = "http://wx.233.com/tiku/exam/reDoExam?md5=93819bcbad70e5c2d568cd52db062ebb&type=1&mode=2&fromUrl=http%3A%2F%2Fwx.233.com%2Ftiku%2Fexam%3FclassId%3D521"
    # if re.findall('?',str):
    #     answ = re.sub(r"，",',',str)
    #     print(answ)
    str = re.findall(r'md5=\S*&',str)
    str =  str[0].split('&')[0]
    print(str)

def addCategory(item):
    string = '2018年初级社会工作者考试《社会工作综合能力》模考大赛试卷三'
    conn = pymysql.connect(host="139.196.177.17", user="root", password="root1234", db="bst", use_unicode=True,charset="utf8")
    cur = conn.cursor()
    # sql = "INSERT INTO page_category (cname,ipid,ENABLE,igrade,isubjectid,icreator,ccreator,dcreator,imodify,cmodify,dmodify) VALUES ('"+item+"',429,0,6,67,1,'admin',now(),1,'admin',now())"
    # sql =
    cur.execute("select * from page_category where cname = %s",[string])
    # conn.commit()
    repetition = cur.fetchone()
    cur.close()
    # return cur.lastrowid
    return repetition[0]

#解析url
def urlparse(url):
    weburl = urlparse3.parse_url(url)
    print(weburl.domain)
    print(weburl.fragment)
    print(weburl.geturl())
    print(weburl.username)
    print(weburl.password)
    print(weburl.path)
    print(weburl.port)
    print(weburl.query)
    print(weburl.scheme)

if __name__ == '__main__':
    # qanswers = answers()
    # print(qanswers)
    # method()
    # urlparse('http://admin:secret@local-domain.com:8000/path?q=123#anchor')
    id = addCategory(None)
    print(id)

