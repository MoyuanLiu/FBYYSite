


def readfileaslist(filename):
    file_handle = open(filename, encoding='utf-8', errors="ignore")
    content = file_handle.read()
    contentlist = []
    if content.strip():
        contentlist = content.split('\n')
    file_handle.close()
    return contentlist


def writelineslist(filename, contentlist):
    file_handle = open(filename, 'w', encoding='utf-8', errors="ignore")
    resultlist = []
    for i in range(0, len(contentlist)):
        if i == len(contentlist) - 1:
            resultlist.append(contentlist[i])
        else:
            resultlist.append(contentlist[i] + "\n")
    file_handle.writelines(resultlist)
    file_handle.close()


def removelineitem(filename, targetstr):
    contentlist = readfileaslist(filename)
    if targetstr in contentlist:
        contentlist.remove(targetstr)
        writelineslist(filename, contentlist)


def appendlineitem(filename, targetstr):
    file_handle = open(filename, 'a+', encoding='utf-8', errors="ignore")
    file_handle.write(targetstr + "\n")
    file_handle.close()


def clearfile(filename):
    file_handle = open(filename, 'w', encoding='utf-8', errors="ignore")
    file_handle.truncate()
    file_handle.close()