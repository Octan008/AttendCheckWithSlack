"""testapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from register import urls
from attendance.views import ApiErrorView, RegisterView, OathView, Ver_Red_View, LogView, LogEditView, SignInOathView, LandingView

urlpatterns = [
    path('admin/', admin.site.urls),
    # # url(r'^kintai/', include('kintai.urls')), 
    # path('admin/', admin.site.urls),
    path('register/', include('register.urls')), 
    path('sapi/', ApiErrorView.as_view()), 
    path('sapi/register', RegisterView.as_view()), 
    path('oath', OathView.as_view()),
    path('signin', SignInOathView.as_view()),
    # path('postrequest', PostRequestView.as_view()),
    path('verification_redirect', Ver_Red_View.as_view()),
    path('logs/', LogView.as_view()),
    path('logs/edit/',LogEditView.as_view()),
    path('',LandingView.as_view())
]
