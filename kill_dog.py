import pandas as pd
import requests
import re
import datetime
import time
import pymysql
import execjs
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] Kill Dog 启动中......')
reg = re.compile(r'<tr class="matchTr" matchid="(.*?)">')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
mp1={'nan':None,'半球': 0.5, '平手': 0, '半/一': 0.75, '平/半': 0.25, '一球': 1, '一/球半': 1.25, '球半': 1.5, '两球': 2, '球半/两': 1.75, '两球/两球半':2.25, '两球半/三球':2.75,
    '三球/三球半':3.25,'两球半/三球':2.75,'两半': 2.5, '两半/三': 2.75, '三球': 3, '两/两半': 2.25, '三/三半': 3.25, '三半': 3.5, '三球半':3.5,'三球半/四球':3.75,'两球半':2.5,'四球/四球半':4.25,
    '四球半/五球':4.75,'四球半':4.5,'五球':5,'半球': 0.5, '平手': 0, '半/一': 0.75, '平/半': 0.25, '一球': 1, '一/球半': 1.25, '球半': 1.5, '两球': 2, '球半/两': 1.75,
    '两球/两球半':2.25, '两球半/三球':2.75,
    '三球/三球半':3.25,'两球半/三球':2.75,'两半': 2.5, '两半/三': 2.75, '三球': 3, '两/两半': 2.25, '三/三半': 3.25, '三半': 3.5, '三球半':3.5,'三球半/四球':3.75,
    '三半/四': 3.75, '四球': 4, '四/四半': 4.25, '四半': 4.5, '四半/五': 4.75, '五球': 5, '半球/一球': 0.75, '一球/球半': 1.25, '球半/两球': 1.75,  '平手/半球': 0.25,
    '五球半/六球':5.75,'五球半':5.5,'六球':6,'五球/五球半':5.25,
    '三半/四': 3.75, '四球': 4, '四/四半': 4.25, '四半': 4.5, '四半/五': 4.75, '五球': 5, '半球/一球': 0.75, '一球/球半': 1.25, '球半/两球': 1.75,  '平手/半球': 0.25}
mp2={'nan':None,'2.5/3球':2.75, '2.5球':2.5, '3球':3, '3.5球':3.5, '3/3.5球':3.25, '2/2.5球':2.25,'2球':2, '1.5/2球':1.75, '1.5球':1.5,
        '3.5/4球':3.75, '4球':4,'3.5球':3.5,'4/4.5球':4.25,'4.5球':4.5,'4.5/5球':4.75,'5.0球':5,'4.75球':4.75,'2.5/3':2.75, '2.5':2.5, '3':3, '3.5':3.5, '3/3.5':3.25, '2/2.5':2.25,'2':2, '1.5/2':1.75, '1.5':1.5,
        '3.5/4':3.75, '4':4,'3.5':3.5,'4/4.5':4.25,'4.5':4.5,'4.5/5':4.75,'5.0':5,'4.75':4.75,'5.5':5.5,'5/5.5':5.25,'5.5/6':5.75,'6':6,'5':5,'nan':None,'2.5/3球':2.75, '2.5球':2.5, '3球':3, '3.5球':3.5, '3/3.5球':3.25, '2/2.5球':2.25,'2球':2, '1.5/2球':1.75, '1.5球':1.5,
        '3.5/4球':3.75, '4球':4,'3.5球':3.5,'4/4.5球':4.25,'4.5球':4.5,'4.5/5球':4.75,'5.0球':5,'4.75球':4.75,'2.5/3':2.75, '2.5':2.5, '3':3, '3.5':3.5, '3/3.5':3.25, '2/2.5':2.25,'2':2, '1.5/2':1.75, '1.5':1.5,
        '3.5/4':3.75, '4':4,'3.5':3.5,'4/4.5':4.25,'4.5':4.5,'4.5/5':4.75,'5.0':5,'4.75':4.75,'5.5':5.5,'5/5.5':5.25,'5.5/6':5.75,'6':6,'5':5,'6.5/7':6.75,'6.5':6.5,'6/6.5':6.25,'7.0':7}

title=["欧主初赔","欧初平赔","欧客初赔","欧主临赔","欧平临赔","欧客临赔","初盘","临盘","主初赔","客初赔","主临赔","客临盘赔","球初盘","球临盘","大球初盘","小球初盘","大球临盘","小球临盘"]
def create_cmd(params,bias):
    try:
        if len(params)==12:
            cmd="""SELECT
                `football_sheet3.0`.`赛果` 
            FROM
                `football_sheet3.0` 
            WHERE
                ABS( %f - `football_sheet3.0`.`欧主初赔` )+ abs( %f - `football_sheet3.0`.`欧初平赔` )+ abs( %f - `football_sheet3.0`.`欧客初赔` )+ abs( %f - `football_sheet3.0`.`欧主临赔` )+ abs( %f - `football_sheet3.0`.`欧平临赔` )+ abs( %f - `football_sheet3.0`.`欧客临赔` )+ abs( %f - `football_sheet3.0`.`初盘` )+ abs( %f - `football_sheet3.0`.`临盘` )+ abs( %f - `football_sheet3.0`.`主初赔` )+ abs( %f - `football_sheet3.0`.`客初赔` )+ abs( %f - `football_sheet3.0`.`主临赔` )+ abs(%f - `football_sheet3.0`.`客临盘赔` )<bias
                ORDER BY ABS( %f - `football_sheet3.0`.`欧主初赔` )+ abs( %f - `football_sheet3.0`.`欧初平赔` )+ abs( %f - `football_sheet3.0`.`欧客初赔` )+ abs( %f - `football_sheet3.0`.`欧主临赔` )+ abs( %f - `football_sheet3.0`.`欧平临赔` )+ abs( %f - `football_sheet3.0`.`欧客临赔` )+ abs( %f - `football_sheet3.0`.`初盘` )+ abs( %f - `football_sheet3.0`.`临盘` )+ abs( %f - `football_sheet3.0`.`主初赔` )+ abs( %f - `football_sheet3.0`.`客初赔` )+ abs( %f - `football_sheet3.0`.`主临赔` )+ abs(%f - `football_sheet3.0`.`客临盘赔` ) LIMIT 5
                """%(tuple(params+params))
        else:
            cmd="""SELECT
                `football_sheet3.0`.`总进球`,
                `football_sheet3.0`.`球临盘` 
                FROM
                    `football_sheet3.0` 
                WHERE
                    abs(%f - `football_sheet3.0`.`球初盘` )+ abs(%f - `football_sheet3.0`.`球临盘` )+ abs(%f - `football_sheet3.0`.`大球初盘` )+ abs(%f - `football_sheet3.0`.`小球初盘` )+ abs(%f - `football_sheet3.0`.`大球临盘` )+ abs(%f - `football_sheet3.0`.`小球临盘` )<bias
                ORDER BY abs(%f - `football_sheet3.0`.`球初盘` )+ abs(%f - `football_sheet3.0`.`球临盘` )+ abs(%f - `football_sheet3.0`.`大球初盘` )+ abs(%f - `football_sheet3.0`.`小球初盘` )+ abs(%f - `football_sheet3.0`.`大球临盘` )+ abs(%f - `football_sheet3.0`.`小球临盘` ) LIMIT 5
                """%(tuple(params+params))

        return cmd.replace('bias',str(bias))
    except :
        return False

def get_articles():
    def concatFullurl(url):return "http://www.310win.com"+url
    at_url='http://www.310win.com/jingcaizuqiu/info_t1sub1page1.html'
    at=requests.get(at_url,headers)
    at_t=pd.read_html(at.text)[1]
    at_links_reg=re.compile(r"""<a href="(.*?)" target="_blank" style='font-weight:bolder;font-size:14px;'>""")
    at_links=list(map(concatFullurl,re.findall(at_links_reg,at.text)))
    for i in range(1,40,2):
        at_t[1][i]=at_links.pop(0)
    at_t2=at_t[at_t.index%2==1]
    at_t1=at_t[at_t.index%2==0]
    at_t1.reset_index(inplace=True)
    at_t2.reset_index(inplace=True)
    at_=pd.DataFrame()
    at_['标题']=at_t1[0]
    at_['时间']=at_t1[1]
    
    at_['简介']=at_t2[0]
    at_['链接']=at_t2[1]
    at_.dropna(inplace=True)
    at_.reset_index(inplace=True)
    del at_['index']
    return at_
def get_color_eggs():
    color_egg_url='http://www.310win.com/jingcaizuqiu/info_t3.html'
    color_egg=requests.get(color_egg_url,headers)
    egg=pd.read_html(color_egg.text)[1]
    del egg[9]
    egg.columns=egg.iloc[0]
    del egg['赔率']
    return egg.iloc[1:].to_html(header = True,index = False).replace('\n','').replace("dataframe",'table')

def get_match_info():
    match_info=[]
    total_match_url='http://www.310win.com/info/match/data/bfdata.js?'+str(int(time.time()))
    total_match=requests.get(total_match_url,headers=headers)
    js_data=execjs.compile(total_match.text.replace('ShowBf();',''))
    match_list=js_data.eval('A')
    match_info_idx=[0,2,5,8,11]
    for m in match_list:
        if not m: continue
        info=[]
        for i in match_info_idx:
            info.append(m[i].replace('<font color=#880000>(中)</font>',''))
        if m[14]!='' and m[15]!='':
            info.append(m[14]+'-'+m[15])
        if m[13]=='-1':info.append('已结束')
        elif m[13]=='3':info.append('正在进行')
        elif m[13]=='2':info.append('状态未知')
        elif m[13]=='0':info.append('未开始')
        match_info.append(info)

    return match_info

class Analyzer():
    def __init__(self,bias):
        self.sheet = pymysql.connect(host='1.116.145.211', port=3306,
                                     user='root', passwd='whatcoldwind', db='my_web_database')
        self.all_match=[]
        self.cursor = self.sheet.cursor()
        self.res = ()
        self.cmd=''
        self.bias=bias
        self.host=''
        self.guest=''
        self.pan=''
    def analyze(self, cmd,is_ball):
        self.cursor.execute(cmd)
        res=self.cursor.fetchall()[:10]
        if len(res)==0:
            return '数据不足分析失败'
        if not is_ball: 
            analyzed_data=[0,0,0]
            for i in res:
                analyzed_data[i[0]]+=1
        
            return analyzed_data
        else:
            is_big_ball=0
            for i in res:
                if i[0]>i[1]:is_big_ball+=1
            pd=''
            if res[0][0]>res[0][1]:
                pd+='大'
            else:
                pd+='小'
            if is_big_ball>=3:
                return pd+'大'
            else:
                return pd+'小'
    def close(self):
        self.sheet.commit()
        self.cursor.close()
        self.sheet.close()
    def analyze_match(self,match_id):
        return self.analyze_single_match([self.get_pan_info(match_id=match_id)])
    def analyze_single_match(self,pan_info):
        try:
            m=0
            params=[]
            zeros=0
            if '受' in str(pan_info[m]['临盘']) :
                pan_info[m]['临盘']=-mp1[pan_info[m]['临盘'][1:]]
            else:pan_info[m]['临盘']=mp1[pan_info[m]['临盘']]
            if '受' in str(pan_info[m]['初盘']) :
                pan_info[m]['初盘']=-mp1[pan_info[m]['初盘'][1:]]
            else:pan_info[m]['初盘']=mp1[pan_info[m]['初盘']]
            pan_info[m]['球临盘'] =mp2[pan_info[m]['球临盘']]
            pan_info[m]['球初盘'] =mp2[pan_info[m]['球初盘']]
            for info in title:
                if pan_info[m][info]==0:
                    zeros+=1
                if str(pan_info[m][info])==str(float('nan')): 
                    zeros=4
                    break
                params.append(float(pan_info[m][info]))
            if zeros>=3:
                return [{'出错了':'盘信息不够'}]
            try:
                ball_cmd=create_cmd(params[12:],self.bias)
                win_cmd=create_cmd(params[:12],self.bias)
                pan_info[m]['胜负预测']=self.analyze(win_cmd,0)
                pan_info[m]['大球预测']=self.analyze(ball_cmd,1)
                self.pan=pan_info[m]['球临盘']
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析成功')
                return pan_info[m]
            except :
                return [{'出错了':'分析失败'}]
        except:
            return [{'出错了':'主循环报错'}]
    def get_pan_info(self,match_id):
        match={}
        try:
            op_url='http://1x2d.win007.com/'+ str(match_id)+'.js'
            op_data=requests.get(op_url,headers=headers)
            op_data_js=execjs.compile(op_data.text)
            last_op=op_data_js.eval('gameDetail')
            org_op=op_data_js.eval('game')
            self.host=op_data_js.eval('hometeam_cn')
            self.guest=op_data_js.eval('guestteam_cn')
            
            avg_org_op=[0,0,0]
            for i in range(len(org_op)):
                org_op[i] = org_op[i].split('|')
                avg_org_op[0]+=float(org_op[i][3])
                avg_org_op[1]+=float(org_op[i][4])
                avg_org_op[2]+=float(org_op[i][5])
            if len(org_op):
                avg_org_op=[avg_org_op[0]/len(org_op),avg_org_op[1]/len(org_op),avg_org_op[2]/len(org_op)]
            avg_last_op=[0,0,0]
            for i in range(len(last_op)):
                last_op[i] = last_op[i].split('|')
                avg_last_op[0]+=float(last_op[i][0][last_op[i][0].index('^')+1:])
                avg_last_op[1]+=float(last_op[i][1])
                avg_last_op[2]+=float(last_op[i][2])
            if len(last_op):
                avg_last_op=[avg_last_op[0]/len(last_op),avg_last_op[1]/len(last_op),avg_last_op[2]/len(last_op)]
            match['欧主初赔']=avg_org_op[0]
            match['欧初平赔']=avg_org_op[1]
            match['欧客初赔']=avg_org_op[2]
            match['欧主临赔']=avg_last_op[0]
            match['欧平临赔']=avg_last_op[1]
            match['欧客临赔']=avg_last_op[2]
            time.sleep(1)
            yp_url='http://www.310win.com/handicap/'+str(match_id)+'.html'
            yp_data=requests.get(yp_url,headers=headers)
            time.sleep(1)
            yp_tb=pd.read_html(yp_data.text)
            yp_tb=yp_tb[1]
            yp_tb.drop(index=[0,1])
            del yp_tb[list(yp_tb.columns)[8]]
            del yp_tb[list(yp_tb.columns)[7]]
            dp=[]
            for i in range(yp_tb.shape[0]):
                if not '金宝博' in yp_tb.iloc[i][0]:dp.append(i)
            yp_tb=yp_tb.drop(index=dp)
            yp_tb=yp_tb.iloc[0].tolist()[1:]
            match['初盘']=yp_tb[1]
            match['临盘']=yp_tb[4]
            match['主初赔']=yp_tb[0]
            match['客初赔']=yp_tb[2]
            match['主临赔']=yp_tb[3]
            match['客临盘赔']=yp_tb[5]
            ball_url='http://www.310win.com/overunder/'+str(match_id)+'.html'
            ball_data=requests.get(ball_url,headers=headers)
            ball_tb=pd.read_html(ball_data.text)[1]
            ball_tb.drop(index=[0,1])
            del ball_tb[list(ball_tb.columns)[8]]
            del ball_tb[list(ball_tb.columns)[7]]
            dp=[]
            for i in range(ball_tb.shape[0]):
                if not '金宝博' in ball_tb.iloc[i][0]:dp.append(i)
            ball_tb=ball_tb.drop(index=dp)
            ball_tb=ball_tb.iloc[0].tolist()[1:]
            match['球初盘']=ball_tb[1]
            match['球临盘']=ball_tb[4]
            match['大球初盘']=ball_tb[0]
            match['小球初盘']=ball_tb[2]
            match['大球临盘']=ball_tb[3]
            match['小球临盘']=ball_tb[5]
            self.pan=match['球临盘']
        except:
            match['初盘']='获取失败'
            match['临盘']='获取失败'
            match['主初赔']='获取失败'
            match['客初赔']='获取失败'
            match['主临赔']='获取失败'
            match['客临盘赔']='获取失败'
            match['欧主初赔']='获取失败'
            match['欧初平赔']='获取失败'
            match['欧客初赔']='获取失败'
            match['欧主临赔']='获取失败'
            match['欧平临赔']='获取失败'
            match['欧客临赔']='获取失败'
            match['球初盘']='获取失败'
            match['球临盘']='获取失败'
            match['大球初盘']='获取失败'
            match['小球初盘']='获取失败'
            match['大球临盘']='获取失败'
            match['小球临盘']='获取失败'
        return match
