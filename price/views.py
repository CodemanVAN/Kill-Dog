from django.shortcuts import render
from price.models import Addkeys
from my_user.models import User
import datetime
from django.contrib.auth.decorators import login_required

import generate
# Create your views here.
@login_required(login_url='/login/')
def viewPrice(request):
    content={}
    testkey=Addkeys()
    testkey.keyString=generate.generateKey()
    testkey.save()
    content['res']=[testkey.keyString,1]
    if request.user.is_authenticated:
        content['username']=request.user.username
    if request.method == 'POST':
        userkey=request.POST.get('key')
        key=Addkeys.objects.filter(keyString=userkey,userName=None).first()
        if key:
            user=User.objects.filter(username=request.user.username).first()
            user.userAnalyzeNum+=20
            user.save()
            key.userName=request.user.username
            key.usedTime=datetime.datetime.now()
            key.save()
            content['res']=['充值成功',1]
        else:content['res']=['卡密不正确或者已经被使用',0]
    return render(request,'price/detail.html',content)