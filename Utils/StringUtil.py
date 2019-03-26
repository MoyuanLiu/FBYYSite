from UserManage.models import *
import re

def generate_permission_range_msg_dict(inputstr):
    inputlist = inputstr.split(',')
    range_dict = {}
    for inputmsg in inputlist:
        departinputmsg = inputmsg.split('-')[0]
        storeinputmsg = inputmsg.split('-')[1]
        if not departinputmsg in range_dict.keys():
            newstorelist = []
            newstorelist.append(storeinputmsg)
            range_dict[departinputmsg] = newstorelist
        else:
            if storeinputmsg == 'All':
                range_dict[departinputmsg].clear()
                range_dict[departinputmsg].append(storeinputmsg)
            else:
                if not 'All' in newstorelist:
                    range_dict[departinputmsg].append(storeinputmsg)
    return range_dict

def parse_permission_range_str(inputstr):
    inputlist = inputstr.split(',')
    range_dict = {}
    departlist = []
    storelist = []
    for inputmsg in inputlist:
        departinputmsg = inputmsg.split('-')[0]
        storeinputmsg = inputmsg.split('-')[1]
        if not departinputmsg in departlist:
            departlist.append(departinputmsg)
        if not storeinputmsg in storelist:
            if storeinputmsg == 'All':
                allstoreobjs = TbStoreInfo.objects.filter(tb_store_info_department_code=departinputmsg)
                for storeobj in allstoreobjs:
                    storelist.append(storeobj.tb_store_code)
            else:
               storelist.append(storeinputmsg)
    range_dict['departlist'] = departlist
    range_dict['storelist'] = storelist

def changeStrtoFloat(targetstr):
    if targetstr!=''and targetstr !='-':
        return float(str.replace(targetstr,',',''))
    else:
        return 0.00


def fixStoreName(inputstr):
    storename = re.sub('\[\w*\]','',inputstr)
    return storename

def getstorecodebyname(inputstr):
    searchObj = re.search('(\[[a-zA-Z]+\d*\])', inputstr, re.M | re.I)
    if searchObj:
        if searchObj.group(1)=="[BTM]":
            return "TM"
        else:
            return searchObj.group(1).replace('[','').replace(']','')
    else:
        return inputstr



def fixSymbol(inputstr):
    if inputstr.find('\'')>0:
        return str.replace(inputstr,'\'','\'\'')
    elif inputstr.find('\\'):
        return str.replace(inputstr,'\\','')
    else:
        return inputstr


def fixNullNumber(inputfloat):
    if inputfloat is None or inputfloat == '':
        return 0
    else:
        return inputfloat


def changeStrtoInt(targetstr):
    if targetstr != ''and targetstr !='-':
        return int(str.replace(targetstr,',',''))
    else:
        return 0


def changeStrtoPercent(targetstr):
    if targetstr != ''and targetstr !='-':
        return float(str.replace(targetstr,'%',''))/100


def extractProductNum(targetstr):
    if targetstr != ''and targetstr !='-' and str.find(targetstr,'p'):
        return str.split(targetstr,'p')[0] + "p"
    else:
        return targetstr


def findImportDate(targetstr):
    searchObj = re.search('\D*(\d+\-\d+\-\d+)', targetstr, re.M | re.I)
    if searchObj:
        return searchObj.group(1)
    else:
        return targetstr


def changeFloattoInt(input):
    return int(input)


def changeExcelDate(datestamp):
    delta = datetime.timedelta(days=datestamp)
    targetday = datetime.datetime.strptime('1899-12-30','%Y-%m-%d')+delta
    return datetime.datetime.strftime(targetday,'%Y-%m-%d')


def fixNull(target):
    if target is None or target=='':
        return 'null'
    else:
        return target


def fixchangeline(inputstr):
    if inputstr != '' and str.find(inputstr,'\n'):
        return str.replace(inputstr,'\n','\\n')
    else:
        return inputstr


def removespace(inputstr):
    if inputstr != '':
        return str.replace(inputstr,' ', '')
    else:
        return inputstr


def getdatestr(inputstr):
    pattern = r'\d{4}/\d{1,2}/\d{1,2}'
    if re.match(pattern,inputstr):
        return re.findall(pattern,inputstr)[0]
    else:
        return ''
