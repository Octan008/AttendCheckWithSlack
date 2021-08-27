import sys
from types import ModuleType
# from django.conf import settings
from testapp import urls_tenants

from django.contrib import admin
from django.urls import path, include

# from testapp import urls_tenants

from attendance.views import LogView, LogEditView#, ValidView


def generate_tenant_url_module(tenant) -> str:

    tenant_prefex = 't/'+tenant.schema_name
    urlpatterns = [
        path(tenant_prefex+'/admin/', admin.site.urls),
        path('sapi/', include('attendance.urls')),
        path(tenant_prefex+'/register/', include('register.urls')), 
        # path(tenant_prefex+'/validation/', ValidView.as_view(), name="random_form"), 
        path(tenant_prefex+'/logs/', LogView.as_view()), 
        path(tenant_prefex+'/logs/edit/', LogEditView.as_view()), 
    ]
    module_name = "tenant_urls_{0}".format(tenant.schema_name)
    mod = ModuleType(module_name)
    mod.urlpatterns = urlpatterns
    sys.modules[module_name] = mod

    return module_name