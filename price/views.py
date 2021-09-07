from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login/')
def viewPrice(request):
    content={}
    if request.user.is_authenticated():
        content['username']=request.user.username
    return render(request,'price/detail.html',content)