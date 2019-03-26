import re
def fixStoreName(inputstr):
    storename = re.sub('\[\w*\]','',inputstr)
    return storename

def getstorecodebyname(inputstr):
    searchObj = re.search('(\[[a-zA-Z]+\d*\])', inputstr, re.M | re.I)
    if searchObj:
        if searchObj.group(1)=="[BTM]":
            return "[TM]"
        else:
            return searchObj.group(1)
    else:
        return inputstr
print(getstorecodebyname("[淘宝]BOB[BTM]密斯特顾777"))
