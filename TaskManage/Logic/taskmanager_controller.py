
from TaskManage.Logic.backgroundtask_controller import *

def get_all_users_by_account(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user.tb_user_info_issuperuser:
        return TbUserInfo.objects.all()
    else:
        return -1

def get_task_list_by_user(account):
    user = TbUserInfo.objects.get_user_by_account(account)
    if user.tb_user_info_issuperuser:
        return TbTaskInfo.objects.all()
    else:
        userid = user.idtb_user_info
        return TbTaskInfo.objects.filter(tb_task_info_user_id=userid)

def task_info_list(alltasklist):
    for task in alltasklist:
        taskcontentdict = {}
        taskcontentdict['fileuploadname']=(json.loads(task.tb_task_info_content)["fileuploadname"])
        taskcontentdict['savepathname'] = (json.loads(task.tb_task_info_content)["savepathname"])
        taskcontentdict['taskusernickname'] = TbUserInfo.objects.get_user_by_id(task.tb_task_info_user_id).tb_user_info_nickname
        task.tb_task_info_content = taskcontentdict
    return alltasklist

def get_current_user(account):
    return TbUserInfo.objects.get_user_by_account(account)

def runbackgroundserver():
    gettaskconditionlist=[]
    gettaskconditionlist.append('任务未完成')
    gettaskconditionlist.append('任务进行中')
    runtaskcondition = Q()
    runtaskcondition.children.append(('tb_task_info_status__in', gettaskconditionlist))
    while True:
        expiretaskbyexpiredate()
        runtasklist = TbTaskInfo.objects.order_by('tb_task_info_createtime').filter(runtaskcondition)[0:1]
        if runtasklist:
            for runtask in runtasklist:
                runtask.tb_task_info_status = '任务进行中'
                runtask.save()
                runimporttask(runtask)
        else:
            print('暂时没有任务休眠5秒')
            time.sleep(5)