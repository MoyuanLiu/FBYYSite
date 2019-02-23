import time
teststr ='2018/12/29'
print(time.strptime(teststr,'%Y/%m/%d').replace('/','-'))
