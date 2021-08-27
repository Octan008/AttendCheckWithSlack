from .views import TenantViewRandomForm

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', TenantViewRandomForm.as_view(), name="random_form"),
]
