#_*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import os
import re
import xlwt

# 设置请求头文件
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
            'referer':'http://wx.233.com/tiku/chapter/623'#伪造一个访问来源 "http://www.mzitu.com/100260/2"
}
payload = {
    "account": "&lt;15715219240&gt;",
    "password": "&lt;441852&gt;"
}
session_requests = requests.session()

content = requests.get("http://wx.233.com/tiku/chapter/623",headers=headers)



n = 1
bsSearchText = BeautifulSoup(content.text,'lxml').find('div',class_='lo-tablecon')
while n<10:
    subnum = bsSearchText.find_all('tbody')[n].find('tr')['data-childcount']
    i = 1
    subjectTitle = bsSearchText.find_all('tbody')[n].find('tr').find('td').get_text()
    print(subjectTitle)
    while i <= int(subnum):
        all_text = bsSearchText.find_all('tbody')[n].find_all('tr')[i].find_all('td')[0].get_text()
        print(all_text)
        i+=1
    n += 1

#创建一个Excel文档
#workbook = xlwt.Workbook(encoding='utf-8',style_compression=0);
#创建一个sheet
#sheet = workbook.add_sheet('章节',cell_overwrite_ok=True)
#写入数据
#sheet.write(row,col,text)
#保存
#workbook.save(r'E:\test1.xls')