from django.core.management.base import BaseCommand
 

from celery import shared_task
# from .models import Repository
from tenants.models import Client
from attendance.models import *
from attendance.AttendFuncs import SlackSend


from django.db import connection, utils
from django.utils import timezone
from django.utils.timezone import localtime # 追加

class Command(BaseCommand):
    # def handle(self, *args, **options):
    #     for i in range(100):
    #         print('Hello Medium! ', end='')

    # @shared_task
    def handle(self, *args, **options):
        print("Start:payoff", localtime(timezone.now()), localtime(timezone.now()).day);
        for tenant in Client.objects.all():
            connection.set_tenant(tenant)
            conf = Config.objects.all()
            if conf.exists():
                conf=conf.first()
                if conf.payoff_date == localtime(timezone.now()).day:
                    for user in User.objects.all():
                        login = user.if_login
                        if(user.last_payoff != None):
                            records = user.username_log.filter(if_payoff = False, id__gt = user.last_payoff.id);
                        else:
                            records = user.username_log.filter(if_payoff = False);
                        sum_time = 0
                        if login:
                            omit_record = user.login_record
                            for record in records:
                                if record != omit_record:
                                    sum_time += record.net_time
                                    record.if_payoff=True
                                    record.save()
                                    user.last_payoff = record
                                    user.save()
                        else:
                            for record in records:
                                sum_time += record.net_time
                                record.if_payoff=True
                                record.save()
                                user.last_payoff = record
                                user.save()
                        # message = message+user.user_name+" : "+str(sum_time)+"\n"
                        message="精算が完了しました"

                        noti_message=user.real_name+"さんの今月の稼働時間合計: "+str(sum_time)+"分\n"
                        if conf.if_notice_payoff_to_admins:
                            admins = conf.admin_users.split(',')
                            for admin in admins:
                                SlackSend("@"+admin, "【管理者通知】"+noti_message)
                        if conf.if_notice_payoff_to_users:
                            SlackSend("@"+user.user_name, noti_message)
