from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView, UpdateView

from django.db import connection

from django.urls import reverse

from tenants.models import Client, Domain

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse
from urllib.parse import parse_qs, urlencode

# import datetime
from django.utils import timezone


from attendance.AttendFuncs import *
from attendance.models import *

from django.db import connection, utils

from django.db.models import Prefetch

import os
import json
import requests


from django_tenants.urlresolvers import reverse_lazy
from .forms import GenerateValidForm, LogEditForm, LogForm, AddLogEditFields

from django.utils.dateparse import parse_datetime

import abc

class ApiView(View):
    pass
class BaseFormView(FormView, metaclass=abc.ABCMeta):
    def Signed_get(self, cookie, request,*args, **kwargs):
        return super().get(request,*args, **kwargs)  

    def UnSigned_get(self, cookie, request,*args, **kwargs):
        return self.Signed_get(cookie, request,*args, **kwargs)

    def get(self, request,*args, **kwargs):
        cookie=Cookie.GetCookie(request)
        if Cookie.Cookie_valid(cookie):
            try: 
                tenant=Client.objects.filter(schema_name=cookie['team_id']).first()
                connection.set_tenant(tenant)#テナントの登録
            except:
                return self.UnSigned_get(cookie, request,*args, **kwargs)
            return self.Signed_get(cookie, request,*args, **kwargs)
        else:
            return self.UnSigned_get(cookie, request,*args, **kwargs)

    def Signed_post(self, cookie, request,*args, **kwargs):
        return super().post(request,*args, **kwargs)  

    def UnSigned_post(self, cookie, request,*args, **kwargs):
        return self.Signed_post(cookie, request,*args, **kwargs)
        
    def post(self, request,*args, **kwargs):
        cookie=Cookie.GetCookie(request)
        if Cookie.Cookie_valid(cookie):
            try: 
                tenant=Client.objects.filter(schema_name=cookie['team_id']).first()
                connection.set_tenant(tenant)#テナントの登録
            except:
                return self.UnSigned_post(cookie, request,*args, **kwargs)
            return self.Signed_post(cookie, request,*args, **kwargs)
        else:
            return self.UnSigned_get(cookie, request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Signed'] = Cookie.Cookie_valid(Cookie.GetCookie(self.request))
        if context['Signed']:
            context['team_name']=Data.objects.all().first().team_name
        return context


class BaseTemplateView(TemplateView,  metaclass=abc.ABCMeta):
    def Signed_get(self, cookie, request,*args, **kwargs):
        return super().get(request,*args, **kwargs)  

    def UnSigned_get(self, cookie, request,*args, **kwargs):
        return self.Signed_get(cookie, request,*args, **kwargs)

    def get(self, request,*args, **kwargs):
        cookie=Cookie.GetCookie(request)
        if Cookie.Cookie_valid(cookie):
            try: 
                tenant=Client.objects.filter(schema_name=cookie['team_id']).first()
                connection.set_tenant(tenant)#テナントの登録
            except:
                return self.UnSigned_get(cookie, request,*args, **kwargs)
            return self.Signed_get(cookie, request,*args, **kwargs)
        else:
            return self.UnSigned_get(cookie, request,*args, **kwargs)

    def Signed_post(self, cookie, request,*args, **kwargs):
        return super().post(request,*args, **kwargs)  

    def UnSigned_post(self, cookie, request,*args, **kwargs):
        return self.Signed_post(cookie, request,*args, **kwargs)
        
    def post(self, request,*args, **kwargs):
        cookie=Cookie.GetCookie(request)
        if Cookie.Cookie_valid(cookie):
            try: 
                tenant=Client.objects.filter(schema_name=cookie['team_id']).first()
                connection.set_tenant(tenant)#テナントの登録
            except:
                return self.UnSigned_get(cookie, request,*args, **kwargs)
            return self.Signed_post(cookie, request,*args, **kwargs)
        else:
            return self.UnSigned_post(cookie, request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Signed'] = Cookie.Cookie_valid(Cookie.GetCookie(self.request))
        if context['Signed']:
            context['team_name']=Data.objects.all().first().team_name
        return context


class PersonalTemplateView(BaseTemplateView):
    pass

class PersonalFormView(BaseFormView):
    pass

class MessageView(BaseTemplateView):
    template_name='message.html'