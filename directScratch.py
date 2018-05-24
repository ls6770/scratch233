import requests
from bs4 import BeautifulSoup
import os
import xlwt
import re

#生成Excel文档
book= xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('题目',cell_overwrite_ok= True)
#复制网页，直接抓提
htmlfile = open('G:/test.html','r',encoding='utf-8') #只读方式打开本地文件
result = htmlfile.read()
#result = requests.get('http://localhost:8088/bst/wxlogin/test')

questions_num = BeautifulSoup(result,'lxml').find('div',id='m__progress').find('div',class_='txt').get_text()
s = questions_num.split(r'/')[1]
num1 = re.sub("\D", "", s)
print(int(num1))
n = 0
excelname = BeautifulSoup(result,'lxml').find('div',class_='adress').find_all('a')[2].get_text()
soup = BeautifulSoup(result,'lxml').find('div',id='questionModule').find('ul')
while n < int(num1):
    title = soup.find_all('div',class_='sub-dotitle')[n].get_text() #题目标题
    sheet.write(n,0,str(title))
    answers = soup.find_all('dl',class_='sub-answer')[n].get_text() # 题目选项
    sheet.write(n,1,str(answers))
    right = soup.find_all('div',class_='reck')[n].find('em',class_='right').get_text() # 正确答案
    #right = soup.find_all('div',class_='solution')[n].find_all('li')[0].find('div',class_='wenzi').get_text() # 正确答案
    sheet.write(n,2,str(right))
    jxcontent = soup.find_all('div',class_='solution')[n].find_all('li')[2].find('div',class_='wenzi').get_text() # 解析
    #jxcontent = soup.find_all('div',class_='solution')[n].find_all('li')[3].find('div',class_='wenzi').get_text() # 解析
    sheet.write(n,3,str(jxcontent))
    n +=1

book.save(r'G:/questions/'+excelname+'.xls')

#print(htmlcontent)