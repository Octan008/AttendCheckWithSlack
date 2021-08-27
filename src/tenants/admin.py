from django.contrib import admin
from .models import Client, Domain
from django_tenants.admin import TenantAdminMixin

# Register your models here.
@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')
    # pass

@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
    pass