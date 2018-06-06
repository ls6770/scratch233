# -*- coding: utf-8 -*-
#导入Excel表格模块

import xlwt
#创建一个workbook对象，这就相当于创建了一个Excel文件
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
'''
workbook类初始化时有encoding和style_compression参数
encoding:设置字符编码，一般要这样设置：w = Workbook(encoding='utf-8')，就可以在excel中输出中文了。
默认是ascii。当然要记得在文件头部添加：
#!/usr/bin/env python
# -*- coding: utf-8 -*-
style_compression:表示是否压缩，不常用。
'''
#创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
#在电脑邮件新建一个Excel文件，期中就包含sheet1，sheet2，sheet3三张表
sheet = book.add_sheet('题目',cell_overwrite_ok= True)
#期中的引号中是这张表的名字，cell_overwrite_ok表示是否可以覆盖单元格，其实是workbook实例化的一个参数，默认值是False
#向表中添加数据
sheet.write(0,0,'Englishname') # 其中0-行，0-列指定表中的单元，后是向该单元写入的内容
sheet.write(1,0,'Marcovaldo')
txt1 = '中文名字'
sheet.write(0,1,txt1) # 此处需要将中文字符串解码成Unicode码，否则会报错
txt2 = '马可瓦多'
sheet.write(1,1,txt2)

#最后，将以上操作保存到指定的Excel文件中
book.save(r'E:\test1.xls')