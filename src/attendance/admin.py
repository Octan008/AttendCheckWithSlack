from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(AttendLog)
class AttendLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass
@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass