# -*- coding:utf-8 -*-
try:
    import openpyxl
except:
    import openpyxl
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

print "start load"
#try:
book=openpyxl.load_workbook(r"D:\Code\Python\2018Summer\2018Summer\2_0_temp.xlsx")
print "load success"
sheet=book['Sheet1']
rs=sheet.iter_rows()
for row in rs:
    for col in row:
        print col.value,
    print
book.close()
'''
except:
    print "load fail"
finally:
    print "finish"
'''

##error:
'''
发生了 UnicodeEncodeError
  Message='gbk' codec can't encode character u'\ue863' in position 1: illegal multibyte sequence
  StackTrace:
<module> 中的 D:\Code\Python\2018Summer\2018Summer\2_0_read.py:18
'''