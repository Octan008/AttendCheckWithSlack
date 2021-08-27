from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView, UpdateView

from django.db import connection

from django.urls import reverse

from tenants.models import Client, Domain

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse
from urllib.parse import parse_qs, urlencode

from datetime import datetime, date

from django.utils import timezone
import calendar
# import datetime


from attendance.AttendFuncs import *
from attendance.models import *

from django.db import connection, utils

from django.db.models import Prefetch

import os
import json
import requests


from django_tenants.urlresolvers import reverse_lazy
# from .forms import GenerateValidForm, LogEditForm, LogForm, AddLogEditFields
from .forms import *

from django.utils.dateparse import parse_datetime

from .classes import *




def convert_to_minutes(deltasecond):
    return deltasecond//60

class LandingView(BaseTemplateView):
    template_name='landing.html'

class LoginView(View):
    def post(self, request,*args, **kwargs):
        
        att = ManUser(request)
        conf= Config.objects.all().first()

        message = "エラーが発生しました"
        if(att.if_login()):
            message = "すでにログインしています"
        else:
            new_log = AttendLog(
                user_name = att.thisuser()
            )
            new_log.save()
            att.SetLoginRecord(new_log)
            # message = str(att.username())+"がログインしました" 
            message="ログインしました"

            att.SetLogin()
            att.save()  

            noti_message=str(att.realname())+"がログインしました" 
            if conf.if_send_to_admin:
                admins = conf.admin_users.split(',')
                for admin in admins:
                    att.SlackSend("@"+admin, noti_message)
            if conf.if_send_to_channel:
                att.SlackSend(att.command_channel(), noti_message)

            
        
        return HttpResponse(message)
        
    def get(self, request,*args, **kwargs):
        return HttpResponse("message")
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

class LogoutView(View):
    # @csrf_exempt
    def post(self, request,*args, **kwargs):

        att = ManUser(request)
        conf= Config.objects.all().first()
        
        message = "エラーが発生しました"
        if(not att.if_login()):
            message = "ログインしていません"
        else:
            old_log = att.GetLoginRecord()
            buf_old_log = timezone.now()
            old_log.net_time = convert_to_minutes((buf_old_log - old_log.login_time).seconds)
            old_log.logout_time = buf_old_log
            old_log.save()
            message = "ログアウトしました"

            att.SetLogout()
            att.save()  

            noti_message=att.realname()+"がログアウトしました\n"+"稼働時間："+ str(old_log.net_time) + "分"
            if conf.if_send_to_admin:
                admins = conf.admin_users.split(',')
                for admin in admins:
                    att.SlackSend("@"+admin, noti_message)
            if conf.if_send_to_channel:
                att.SlackSend(att.command_channel(), noti_message)

        return HttpResponse(message)

    def get(self, request,*args, **kwargs):
        return HttpResponse("message")
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

class ApiErrorView(View):
    def post(self, request,*args, **kwargs):
        return HttpResponse("無効なリクエストです")
    def get(self, request,*args, **kwargs):
        return HttpResponse("message")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ApiErrorView, self).dispatch(*args, **kwargs)

class AlreadyRegisterView(View):
    def post(self, request,*args, **kwargs):
        channel=parse_qs(request.body)[b'channel_id'][0].decode('utf-8')
        blocks=[
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Button",
						"emoji": True
					},
					"value": "click_me_123",
                    "url": "https://slackattend.work/postrequest"
				}
			]
		}
	]

        SlackSend(channel, "登録！", blocks)
        message = "すでに登録されています"
        return HttpResponse(message)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(AlreadyRegisterView, self).dispatch(*args, **kwargs)
        
class RegisterView(View):
    def post(self, request,*args, **kwargs):
        message="https://"+os.environ.get('SERVER_DOMAIN')+"/oath"
        channel=parse_qs(request.body)[b'user_name'][0].decode('utf-8')

        att=[
        ]

        SlackSend(channel, "登録！", att)
        return HttpResponse(message)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)



#==========================超えられない壁==================================





class LogView(BaseFormView):    
    form_class = LogForm
    template_name='attend_log_form.html'
    success_url = reverse_lazy('attend_log_form')

    def UnSigned_get(self, cookie, request,*args, **kwargs):
        code = request.GET.get('code', False)
        if code:  
            message="認証に失敗しました"
            send_url="https://slack.com/api/oauth.v2.access"
            headers={
                "Content-Type":"application/x-www-form-urlencoded"
                }
            item_data={
                "client_id":os.environ.get('CLIENT_ID'),
                "client_secret":os.environ.get('CLIENT_SECRET'),
                "code":code,
                "redirect_uri":os.environ.get('REDIRECT_URI_SIGNIN')
                }
            r_post = requests.post(send_url, headers=headers, data=item_data)
            r_post=json.loads(r_post.text)
            if(r_post['ok']):
                try:
                    # if True:
                    response=redirect("./")
                    response.set_cookie(key="SLattend_id", value="Cookiemans2", max_age=60*60*24)
                    response.set_cookie(key="user_id", value=r_post['authed_user']['id'], max_age=60*60*24)
                    response.set_cookie(key="team_id", value=r_post['team']['id'], max_age=60*60*24)
                    return response
                except:
                    message="ログインに失敗しました"+str(r_post)
            return render(request, 'message.html', {'headline':"Error",'message': message})

        return redirect("https://"+os.environ.get('SERVER_DOMAIN')+"/signin")

    def get_context_data(self, **kwargs):
        if True:
            user_id = self.request.COOKIES['user_id']
            team_id = self.request.COOKIES['team_id']
            user = User.objects.filter(user_id=user_id)
            if not user.exists():
                MakeUser(user_id)

            context = super().get_context_data(**kwargs)
            # if(self.request.POST.get('ids', False)):
            context['update_message']=""

            context['real_name']=user.first().real_name
            context['user_id']=user.first().user_id
            context['team_id']=team_id
            context['avatar_url']=json.loads(user.first().profiles)['image_72']

            year = self.request.GET.get('year', self.request.POST.get('year', timezone.now().year))
            term = self.request.GET.get('term', self.request.POST.get('term', timezone.now().month))

            first_date=date(int(year), int(term), 1);
            last_date=date(int(year), int(term), calendar.monthrange(int(year), int(term))[1])
            context['year'] = year
            context['term'] = term

            context['prev_link']="?year="+str(year if term!='1' else int(year)-1)+"&term="+str(int(term)-1 if term!='1' else 12);
            context['next_link']="?year="+str(year if term!='12' else int(year)+1)+"&term="+str(int(term)+1 if term!='12' else 1);
            if user.first().if_login:
                context['data']=user.first().username_log.filter(logout_time__date__range = (first_date, last_date)).exclude(id=user.first().login_record.id)
            else:
                # print(date(2020, 5, 1))
                
                context['data']=user.first().username_log.filter(logout_time__date__range = (first_date, last_date))
            sum_minutes=0
            for record in context['data']:
                sum_minutes = sum_minutes+record.net_time     
            context['sum_minutes'] = sum_minutes
            context['sum_pay'] = (sum_minutes*user.first().payrate)//60          
            
            context['editlink']= "https://"+os.environ.get('SERVER_DOMAIN')+self.request.path+"edit/"
            return context
    

    def form_valid(self, form):   
        if self.request.POST.get('type', "admin") == "table":
            ids = self.request.POST.get('ids', False)
            if ids:
                ids = ids.split(',')
                for i in ids:
                    record=AttendLog.objects.filter(id=i).first()
                    record.login_time=parse_datetime(self.request.POST['login_time'+str(i)])
                    record.logout_time=parse_datetime(self.request.POST['logout_time'+str(i)])
                    record.net_time=convert_to_minutes((record.logout_time - record.login_time).total_seconds())
                    record.save()
            context=self.get_context_data()

            context['update_message']="update"
            response=self.render_to_response(context)

            return response
        else:
            return HttpResponse("https://"+os.environ.get('SERVER_DOMAIN')+"/logs")
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LogView, self).dispatch(*args, **kwargs)


class LogEditView(BaseFormView):
    form_class = LogEditForm
    template_name='attend_log_edit.html'
    success_url = reverse_lazy('attend_log_edit')

    def get(self, request,*args, **kwargs):
        return redirect("https://"+os.environ.get('SERVER_DOMAIN')+"/logs")

    def UnSigned_post(self, cookie, request,*args, **kwargs):
        return redirect("https://"+os.environ.get('SERVER_DOMAIN')+"/logs")

    def get_context_data(self, **kwargs):
        form=LogEditForm()
        user_id = self.request.POST.get('user_id', "admin")
        team_id = self.request.POST.get('team_id', "admin")
        real_name = self.request.POST.get('real_name', "admin")

        # tenant=Client.objects.filter(schema_name=team_id).first()
        # connection.set_tenant(tenant)#テナントの登録
        if user_id == "admin":
            return render(self.request, 'message.html', {'headline':"Error",'message': "不正なリクエストです"})
        else:
            Data = []
            ids=[]
            for record in User.objects.filter(user_id=user_id).first().username_log.all():
                if self.request.POST.get("select"+str(record.id), False):
                    form = AddLogEditFields(form, record)
                    ids.append(str(record.id))
                    Data.append({
                        'id':record.id,
                        'login_time':form['login_time'+str(record.id)],
                        'logout_time':form['logout_time'+str(record.id)],
                        'net_time':record.net_time
                    })

        context = super().get_context_data(**kwargs)

        context['ids']=','.join(ids)
        context['form']=form
        context['real_name']=real_name
        context['user_id']=user_id
        context['term']=self.request.POST.get('term', None)
        context['year']=self.request.POST.get('year', None)
        context['avatar_url']=json.loads(User.objects.filter(user_id=user_id).first().profiles)['image_72']

        context['data']=Data
        context['editlink']= "https://"+os.environ.get('SERVER_DOMAIN')+self.request.path.split('edit/')[0]
        return context

    def form_valid(self, form):   
        if self.request.POST.get('type', "admin") == "edit":
           return self.render_to_response(self.get_context_data())
        
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LogEditView, self).dispatch(*args, **kwargs)      

class OathView(BaseTemplateView):
    template_name = "register_button.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_id'] = os.environ.get('CLIENT_ID')
        context['redirect_uri'] = os.environ.get('REDIRECT_URI')
        return context

class SignInOathView(BaseTemplateView):
    template_name = "oath_button.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_id'] = os.environ.get('CLIENT_ID')
        context['redirect_uri'] = os.environ.get('REDIRECT_URI_SIGNIN')
        return context

class Ver_Red_View(MessageView):
    def get(self, request,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        code = str(request.GET.get('code', "request_denied"))
        if(code != "request_denied"):
            send_url="https://slack.com/api/oauth.v2.access"
            headers={
                "Content-Type":"application/x-www-form-urlencoded"
                }
            item_data={
                "client_id":os.environ.get('CLIENT_ID'),
                "client_secret":os.environ.get('CLIENT_SECRET'),
                "code":code,
                "redirect_uri":os.environ.get('REDIRECT_URI')
                }
            r_post = requests.post(send_url, headers=headers, data=item_data)
            r_post=json.loads(r_post.text)
            if(r_post['ok']):
                try:
                    
                    tenant = Client(schema_name=r_post['team']['id'],
                                    name=r_post['team']['name'],
                                    paid_until='2016-12-05',
                                    on_trial=False)
                    tenant.save()
                    # Add one or more domains for the tenant
                    domain = Domain()
                    domain.domain = r_post['team']['id']+'.'+os.environ.get('SERVER_DOMAIN') 
                    domain.tenant = tenant
                    domain.is_primary = True
                    domain.save()   

                    connection.set_tenant(tenant)#テナントの登録

                    if Config.objects.all().first() == None:
                        conf = Config(
                            hook_url = str(r_post['incoming_webhook']['url']),
                            access_token = str(r_post['access_token']),
                            admin_users =  ','.join([str(r_post['authed_user']['id'])])
                        )
                        conf.save()
                        data = Data(
                            team_id=r_post['team']['id'],
                            team_name=r_post['team']['name']
                        )
                        data.save()

                        send_url="https://slack.com/api/chat.postMessage"
                        headers={
                            # 'Authorization': 'Bearer {}'.format(Config.objects.all().first().access_token),
                            "Content-Type":"application/x-www-form-urlencoded"
                            }
                        item_data={
                            "token":str(Config.objects.all().first().access_token),
                            "channel":str(r_post['incoming_webhook']['channel_id']),
                            "text":"登録通知"
                            }
                        r_post = requests.post(send_url, headers=headers, data=item_data)
                        context['headline']="登録完了"
                        context['message']="Good Job!"
                    else:                    
                        context['headline']="登録済み"
                        context['message']="アカウントが復活しました"

                except:
                    context['headline']="登録済み"
                    context['message']="お客様のSlackチームはすでに登録されています"

            else:
                context['headline']="認証に失敗しました"
        else:
            context['headline']="ERROR"
            context['message']="原因不明のエラーです"

        return self.render_to_response(context)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Ver_Red_View, self).dispatch(*args, **kwargs)

class SignIn_View(View):
    def get(self, request,*args, **kwargs):
        message="認証に失敗しました"
        code = str(request.GET.get('code', "request_denied"))
        if(code != "request_denied"):

            send_url="https://slack.com/api/oauth.v2.access"
            headers={
                "Content-Type":"application/x-www-form-urlencoded"
                }
            item_data={
                "client_id":os.environ.get('CLIENT_ID'),
                "client_secret":os.environ.get('CLIENT_SECRET'),
                "code":code,
                "redirect_uri":os.environ.get('REDIRECT_URI')
                }
            r_post = requests.post(send_url, headers=headers, data=item_data)
            r_post=json.loads(r_post.text)
            if(r_post['ok']):
                message=str(r_post['team'])
                
                try: 
                    tenant=Client().objects.filter(schema_name=r_post['team']['id']).first()
                    connection.set_tenant(tenant)#テナントの登録

                    user_name=str(r_post['authed_user']['id'])
                except:
                    message="登録がありません"
            else:
                message="リクエスト失敗"

        return HttpResponse(message)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SignIn_View, self).dispatch(*args, **kwargs)

# class ManageView(BaseFormView):
#     def get_context_data(self, **kwargs):
#         form = ManageForm()




