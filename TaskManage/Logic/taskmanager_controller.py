
from TaskManage.Logic.backgroundtask_controller import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.info("线程启动")
    gettaskconditionlist=[]
    gettaskconditionlist.append('任务未完成')
    gettaskconditionlist.append('任务进行中')
    runtaskcondition = Q()
    runtaskcondition.children.append(('tb_task_info_status__in', gettaskconditionlist))
    while True:
        expiretaskbyexpiredate()
        runtasklist = TbTaskInfo.objects.order_by('tb_task_info_createtime').filter(runtaskcondition)[0:1]
        logger.info(runtasklist)
        if runtasklist:
            for runtask in runtasklist:
                runtask.tb_task_info_status = '任务进行中'
                runtask.save()
                runimporttask(runtask)
        else:
            logger.info('暂时没有任务休眠5秒')
            time.sleep(5)

def task_query(formdata):
    condition = Q()
    if formdata['taskcreatedatewhetherflag']:
        condition.children.append(('tb_task_info_createtime__contains', formdata['taskcreatedate'].strftime('%Y/%m/%d')))
    if formdata['taskexpiredateewhetherflag']:
        condition.children.append(('tb_task_info_expire_date', formdata['taskexpiredate'].strftime('%Y/%m/%d')))
    if formdata['taskcanceldatewhetherflag']:
        condition.children.append(('tb_task_info_canceltime__contains', formdata['taskcanceldate'].strftime('%Y/%m/%d')))
    if formdata['taskstartdateewhetherflag']:
        condition.children.append(('tb_task_info_starttime__contains', formdata['taskstartdate'].strftime('%Y/%m/%d')))
    if formdata['taskenddateewhetherflag']:
        condition.children.append(('tb_task_info_endtime__contains', formdata['taskenddate'].strftime('%Y/%m/%d')))


    if formdata['taskid'] != '' and formdata['taskid']:
        condition.children.append(('idtb_task_info', int(formdata['taskid'])))
    if formdata['taskuploadfilename'] != '' and formdata['taskuploadfilename']:
        condition.children.append(('tb_task_info_content__contains', formdata['taskuploadfilename']))
    if formdata['taskuserid'] != '' and formdata['taskuserid']:
        condition.children.append(('tb_task_info_user_id', formdata['taskuserid']))

    query_tasklist = TbTaskInfo.objects.filter(condition)
    return query_tasklist