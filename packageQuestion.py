import pymysql
import re

def searchQuestion(numble):
    # 查询数据库，循环查询numble数量的题目
    conn = pymysql.connect(host="139.196.177.17", user="root", password="root1234", db="bst", use_unicode=True,
                           charset="utf8")
    cur = conn.cursor()
    sql = "select * from page_question limit 0,1000"
    cur.execute(sql)
    get_row = cur.fetchmany(1000)
    print(get_row)
    for item in get_row:
        iquestionid = item[0]
        ctype = item[3]
        isort = item[-6]
        page_question(conn,iquestionid,ctype,isort)
    # conn.commit()
    cur.close()
    return cur.lastrowid

def page_question(conn,iquestionid,ctype,isort):

    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO page_pager_question (ipagerid, iquestionid, iquestiontype, isort, iversion, iscore) VALUES (%s, %s, %s, %s, 0, 0)",
        [(576, iquestionid, ctype, isort)])
    conn.commit()
    cur.close()
    return cur.lastrowid

if __name__=='__main__':
    searchQuestion(1000)