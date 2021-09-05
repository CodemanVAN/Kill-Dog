from django.shortcuts import render
from django.contrib import auth
from my_user.models import User,History
from django.contrib.auth.decorators import login_required
import kill_dog
import pandas as pd
# Create your views here

def userAnalyzematch(request):
    user=User.objects.filter(username=request.user.username).first()
    if user.userAnalyzeNum<=0:return '可用分析次数不足1次，分析失败，请及时充值',0
    match_id=request.POST.get('match_id')
    analyzer=kill_dog.Analyzer(1.5)
    res=analyzer.analyze_match(match_id)
    if '大球预测' in res:
        ans=res['大球预测']
        user.userAnalyzeNum-=1
        user.save()
        record=History()
        record.recordHostteam=analyzer.host
        record.recordAwayteam=analyzer.guest
        record.recordMatchid=match_id
        record.userName=user.username
        record.recordPredict=ans
        record.rcecordPan=str(res['球临盘'])
        record.save()
        return ans,1
    else:
        return '分析失败,本次没有扣除分析次数',0
def updateDatabase(request,match_info):
    if not request.user.is_authenticated: return[]
    endMatch=pd.DataFrame(match_info)
    endMatchID=endMatch[endMatch[6]=='已结束'][0].to_list()
    result=endMatch[endMatch[6]=='已结束'][5].to_list()
    for idx,i in enumerate(endMatchID):
        t=History.objects.filter(recordMatchid=i).all()
        for j in t:
            j.recordResult=sum(map(int,result[idx].split('-')))
            j.save()
    return list(History.objects.filter(userName=request.user.username).all())
def viewHomepage(request): # Homepage handler
    content={}
    if request.method=='POST' and request.user.is_authenticated:
        content['res']=userAnalyzematch(request)
    match_info=kill_dog.get_match_info()
    articles_df=kill_dog.get_articles()
    articles=[]
    for i in range(articles_df.shape[0]):
        li=articles_df.iloc[i].tolist()
        if '标签：' in li[2]:
            tp=li[2].split('标签：')
            li[2]=tp[0]
            li.append(tp[1])
        articles.append(li)
    content['egg']=kill_dog.get_color_eggs()
    content['match_info'] = match_info
    content['matchCount']=len(match_info)
    content['history']=updateDatabase(request,match_info)
    print(content['history'],len(content['history']))
    content['articles']=articles
    if request.user.is_authenticated:
        content['username']=request.user.username
    else:
        content['res']='还请先登陆哦！',0
        content['username']='游客'
    return render(request, 'home_page/home.html',content)
def viewAboutpage(request): # About page handler
    pass