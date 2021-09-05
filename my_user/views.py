from django.shortcuts import render,redirect
import random
from django.contrib import auth
from my_user.models import User
from django.urls import reverse
# Create your views here.
def viewUserdata(request): # Userpage handler
    pass


def createCatpath():
    operator=['+','-']
    
    firstNumber=random.randint(50,100)
    secondNumber=random.randint(1,50)
    operation=random.randint(0,1)
    if operator[operation]=='+':
        answer=firstNumber+secondNumber
    else:
        answer=firstNumber-secondNumber
    return answer,str(firstNumber)+operator[operation]+str(secondNumber)

def checkCatpath(answer,userAnswer):
    if str(answer)!=str(userAnswer):
        return 0
    return 1
def checkLogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=auth.authenticate(username=username,password=password)
    if user:
        auth.login(request,user)
        return '登陆成功',1
    else: return '账号或密码错误',0
def checkRegistration(request):
    res=''
    #print(request.POST.get('reusername') ,request.POST.get('repassword1') ,request.POST.get('repassword2'),1)
    if request.POST.get('reusername') is not None and request.POST.get('repassword1') is not None and request.POST.get('repassword2') is not None:
        name = request.POST.get('reusername')
        password1 = request.POST.get('repassword1')
        password2 = request.POST.get('repassword2')
        if password1!=password2:
            res='两次密码输入不对',0
            return res
        if not User.objects.filter(username=name):
            # 此处的User 是 django 自带的model
            newUser=User.objects.create_user(username=name, password=password1)
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")
            newUser.userHost=ip
            newUser.userEmail=request.POST.get("reemail")
            newUser.userBoss=request.POST.get("invitecode")
            newUser.save()
            res ='注册成功'
            return res,1
        else:
            res= '账号名重复了，换一个吧'
            return res,0
    else:
        res='请填写好注册信息'
        return res,0
def viewUserlogin(request):# userLogin handler
    content={}
    if request.user.is_authenticated:
        content['username']=request.user.username
    else: content['username']='游客'
    if request.method=='POST':
        content['status']=checkCatpath(request.session.get('catpth'),request.POST.get('answer'))
        if not content['status']:
            content['res']='验证码错误'
        else:
            print(request.POST)
            if  request.POST.get('username') and request.POST.get('password'):
                content['res'],content['status']=checkLogin(request)
            else:
                content['res'],content['status']=checkRegistration(request)
    catpth=createCatpath()
    content['catpth']=catpth[1]
    request.session['catpth']=catpth[0]
    return render(request, 'user_page/login.html', content)
def logout(request):# logout handler
    auth.logout(request)
    return redirect(reverse('Userlogin'))