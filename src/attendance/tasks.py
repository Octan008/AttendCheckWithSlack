from celery import shared_task
# from .models import Repository
from tenants.models import Client
from .models import *
from .AttendFuncs import SlackSend


from django.db import connection, utils
from django.utils import timezone

@shared_task
def payoff():
    for tenant in Client.objects.all():
        connection.set_tenant(tenant)
        conf = Config.objects.all()
        if conf.exists():
            conf=conf.first()
            if conf.payoff_date == timezone.now().day:
                for user in User.objects.all():
                    login = user.if_login
                    records = user.username_log.filter(if_payoff = False)
                    sum_time = 0
                    if login:
                        omit_record = user.login_record
                        for record in records:
                            if record != omit_record:
                                sum_time += record.net_time
                                record.if_payoff=True
                                record.save()
                    else:
                        for record in records:
                            sum_time += record.net_time
                            record.if_payoff=True
                            record.save()
                    # message = message+user.user_name+" : "+str(sum_time)+"\n"
                    message="精算が完了しました"

                    noti_message=user.user_name+" : "+str(sum_time)+"\n"
                    if conf.if_notice_payoff_to_admins:
                        admins = conf.admin_users.split(',')
                        for admin in admins:
                            SlackSend("@"+admin, noti_message)
                    if conf.if_notice_payoff_to_users:
                        SlackSend("@"+user.user_name, noti_message)
