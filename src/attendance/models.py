from datetime import datetime, timedelta

from django.utils import timezone
from django.core import validators
from django.db import models

# Create your models here.

class User(models.Model):
    real_name=models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    profiles=models.CharField(max_length=5000, null=True)
    payrate = models.IntegerField(
        verbose_name='時給',
        blank=True,
        null=True,
        default=1000,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(10000)]
    )
    if_login = models.BooleanField(verbose_name="ログイン状態",default=False)
    login_record =  models.ForeignKey("AttendLog", verbose_name="ログインレコード",on_delete=models.SET_NULL,null=True,related_name="+")
    last_payoff = models.ForeignKey("AttendLog", verbose_name="最終計算",on_delete=models.SET_NULL, null=True,blank=True,related_name="+")
    last_really_payoff = models.ForeignKey("AttendLog", verbose_name="最終精算",on_delete=models.SET_NULL,null=True,blank=True,related_name="+")
    def __str__(self):
        return self.user_name

class AttendLog(models.Model):
    user_name = models.ForeignKey(User, verbose_name='ユーザ',on_delete=models.PROTECT,related_name='username_log')
    login_time = models.DateTimeField(
        verbose_name='LoginTime',
        blank=True,
        null=True,
        default=timezone.now
    )
    logout_time = models.DateTimeField(
        verbose_name='LogoutTime',
        blank=True,
        null=True,
        default=timezone.now
    )
    net_time = models.IntegerField(
        verbose_name='',
        blank=True,
        null=True,
        default=0,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(2000)]
    )
    if_payoff = models.BooleanField(verbose_name='計算済み',default=False)
    if_really_payoff = models.BooleanField(verbose_name='精算済み',default=False)
    def __str__(self):
        return str(self.user_name)+str(self.login_time)

class Config(models.Model):
    hook_url=models.CharField(max_length=80)
    admin_users =  models.CharField(max_length=20)
    access_token = models.CharField(max_length=60)
    default_payrate = models.IntegerField(
        verbose_name='デフォルト時給',
        blank=True,
        null=True,
        default=1000,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(10000)]
    )
    if_send_to_channel = models.BooleanField(verbose_name='チャンネル通知',default=False)
    if_send_to_admin = models.BooleanField(verbose_name='管理者通知',default=False)
    if_notice_payoff_to_users = models.BooleanField(verbose_name='ユーザへの月末報告',default=False)
    if_notice_payoff_to_admins = models.BooleanField(verbose_name='管理者への月末報告',default=False)
    payoff_date=models.IntegerField( 
        default=1,
        blank=False,
        null=False,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(31)]
    )
class Data(models.Model):
    team_id=models.CharField(max_length=80)
    team_name=models.CharField(max_length=80)
    