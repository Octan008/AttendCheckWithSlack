from django.contrib import admin

# Register your models here.

from .models import Tenants

@admin.register(Tenants)
class TenantAdmin(admin.ModelAdmin):
    pass