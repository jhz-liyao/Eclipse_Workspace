# coding=gbk
'''
@author: liyao
''' 
# b = 0;
# for a in range(1,100,3):
#     b+=a;
# print(b) 
#Enter a code
# print (45678+0x12fd2)
# print ('Learn Python in imooc')
# print (100<99)
# print (0xff==255)
# for x in range(0,100): 
#     if (x > 10) & (x/10 < x % 10):
#         print(x)
# d = {
#     'Adam': 95,
#     'Lisa': 85,
#     'Bart': 59
# }
# print ('Adam',d.get('Adam'))
# print ('Lisa',d.get('Lisa'))
# print ('Bart',d.get('Bart'))
# d = {
#     'Adam': 95,
#     'Lisa': 85,
#     'Bart': 59
# }
# for a,v in d.items():
#     print (a,v) 
import urllib.request
response = urllib.request.urlopen("http://www.baidu.com" )
print(response.getcode())

 