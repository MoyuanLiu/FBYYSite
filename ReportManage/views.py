from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ReportManage.models import *
from ReportManage.Form.Forms import *
from UserManage.Logic.usermanage_controller import get_all_departments
from ReportManage.Logic.cts_controller import *

# Create your views here.
@csrf_exempt
def ctsmanage(request,pagenum):
    ctslist = TbCts.objects.all().order_by('-tb_cts_cal_date')
    paginator = Paginator(ctslist, 8)
    totalpages = paginator.num_pages
    queryform = CtsQueryForm()
    makeform = CtsMakeForm()
    currentpage = pagenum
    departments = get_all_departments()
    try:
        ctslist = paginator.page(currentpage)
    except PageNotAnInteger:
        currentpage = 1
        ctslist = paginator.page(currentpage)
    except EmptyPage:
        currentpage = totalpages
        ctslist = paginator.page(currentpage)
    return render(request, "cts_manage.html", locals())

def ctsquery(request,pagenum):
    return

def ctsmake(request):
    if request.method == "POST":
        form = CtsMakeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            orderexistsflag=ctsordercheck(cd)
            if orderexistsflag:
                createctsdata(cd)
                return render(request,'make_result.html',{'alertmsg':'success'})
            else:
                return render(request, 'make_result.html', {'alertmsg': 'fail','alertdetail':'没有报表制作所需数据！！！'})
        else:
            return render(request,'make_result.html',{'alertmsg':'warning'})