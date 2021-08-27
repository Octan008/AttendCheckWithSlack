from attendance.models import *

from tenants.models import Client, Domain
import json
from urllib.parse import parse_qs

import requests



def MakeUser(user_id, user_name=False):
    send_url="https://slack.com/api/users.info"
    headers={
        "Content-Type":"application/x-www-form-urlencoded"
        }
    item_data={
        "token":Config.objects.all().first().access_token,
        "user":user_id
        }
    r_post = requests.post(send_url, headers=headers, data=item_data)
    r_post=json.loads(r_post.text)

    if not user_name:
        user_name=r_post['user']['name']
    
    new_user = User(
        real_name=str(r_post['user']['real_name']),
        user_name =user_name,
        user_id = user_id,
        profiles = json.dumps(r_post['user']['profile']),
        payrate = 1000,
        if_login = False,
        login_record =  None,
        last_payoff = None,
        last_really_payoff = None
    )
    new_user.save()
    return User.objects.filter(user_name=user_name).first()
                # return "koko"


def SlackSend(channel_id, message, blocks=None):
    send_url="https://slack.com/api/chat.postMessage"
    headers={
        # 'Authorization': 'Bearer {}'.format(Config.objects.all().first().access_token),
        "Content-Type":"application/x-www-form-urlencoded"
        # "Content-Type":"application/json"
        }
    item_data={
        "token":str(Config.objects.all().first().access_token),
        "channel":str(channel_id),
        "text":message
        }
    if blocks:
        item_data["blocks"]=str(blocks)
        pass
    r_post = requests.post(send_url, headers=headers, data=item_data)
    return r_post.ok

class Cookie:
    cookie_dict=["user_id", "team_id", "SLattend_id"]
    @staticmethod
    def SetCookie(response, values):
        # cookie_dict=["user_id", "team_id", "SLattend_id"]
        max_age = 60*60*24
        for key in Cookie.cookie_dict:
            response.set_cookie(key=key, value=values['key'], max_age=max_age)

    @staticmethod
    def GetCookie(request):
        result = {'ok': False}
        # cookie_dict=["user_id", "team_id", "SLattend_id"]
        try:
            if 'SLattend_id' in request.COOKIES:
                for key in Cookie.cookie_dict:
                    result[key] = request.COOKIES[key]
                result['ok']=True
            else:
                result['ok']=False
        except:
            result['ok']=False
        # result['ok']=True
        return result

    @staticmethod
    def Cookie_valid(result):
        return result['ok'] and Client.objects.filter(schema_name=result['team_id']).exists()




class RecordManipuration():
    def __init__(self, request):
        pass       

    def make_data(self, request):
        data = parse_qs(request.body)
        data = {
            "user_id":data[b'user_id'][0].decode('utf-8'),
            "user_name":data[b'user_name'][0].decode('utf-8'),
            "channel_id":data[b'channel_id'][0].decode('utf-8')
        }
        return data
    def SlackSend(self, channel_id, message):
        send_url="https://slack.com/api/chat.postMessage"
        headers={
            # 'Authorization': 'Bearer {}'.format(Config.objects.all().first().access_token),
            "Content-Type":"application/x-www-form-urlencoded"
            }
        item_data={
            "token":str(Config.objects.all().first().access_token),
            "channel":str(channel_id),
            "text":message
            }
        r_post = requests.post(send_url, headers=headers, data=item_data)
        return r_post.ok

class ManUser(RecordManipuration):
    def __init__(self, request):
        self.data = self.make_data(request)
        self.user = self.login_user(self.data)
    def thisuser(self):
        return self.user
    def username(self):
        return self.user.user_name
    def realname(self):
        return self.user.real_name
    def command_channel(self):
        return self.data['channel_id']
    def login_user(self, data):
        username = data['user_name']
        try:
            user = User.objects.filter(user_name=username).first()
            if(user != None):
                return user
            else:
                return MakeUser(str(data['user_id']), str(username))
        except:
            import traceback
            traceback.print_exc()
            return "kokkoyaro"
                
            
    def if_login(self):
        return self.user.if_login

    def SetLogin(self):
        self.user.if_login = True
    def GetLoginRecord(self):
        return self.user.login_record
    def SetLoginRecord(self, logid):
        self.user.login_record = logid
    def SetLogout(self):
        self.user.if_login = False
    def Setid(self, logid):
        self.user.id = logid
    def SetPayoff(self, logid):
        self.user.last_payoff = logid
    def SetRealPayoff(self, logid):
        self.user.last_really_payoff = logid

    def save(self):
        self.user.save()

class Notice(RecordManipuration):
    def __init__(self):
        self.config = Config.objects.first()
    



