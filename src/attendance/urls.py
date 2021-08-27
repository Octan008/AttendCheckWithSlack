from .views import LoginView, LogoutView, LogView, AlreadyRegisterView, OathView #ValidErrorView,  ValidView,

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('logs', LogView.as_view()),
    # path('payoff', PayoffView.as_view()),
    path('register', AlreadyRegisterView.as_view()),
    # path('validation', ValidView),
    path('oath', OathView),
]
# from .models import Config

# if Config.objects.all().first().active == True:
#     urlpatterns = [
#         path('login', LoginView.as_view()),
#         path('logout', LogoutView.as_view()),
#         path('logs', LogView.as_view()),
#         path('payoff', PayoffView.as_view()),
#         path('register', AlreadyRegisterView.as_view()),
#         path('validation', ValidView),
        
#     ]
# else:
#     urlpatterns = [
#         path('<path>/', ValidErrorView.as_view())
#     ]
# urlpatterns = [
#     path('login', LoginView.as_view()),
#     path('logout', LogoutView.as_view()),
#     path('logs', LogView.as_view()),
#     path('payoff', PayoffView.as_view()),
#     path('register', AlreadyRegisterView.as_view()),
#     path('validation', ValidView),
    
# ]