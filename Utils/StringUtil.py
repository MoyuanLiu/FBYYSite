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

