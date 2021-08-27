from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import connection, utils
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin  # todo change

from django_tenants.utils import remove_www_and_dev, get_public_schema_name, get_tenant_domain_model
# from django.db import utils

import os

from django_tenants.middleware.main import TenantMainMiddleware
from tenants.models import Client, Domain
from tenants.urls import generate_tenant_url_module

import json
from urllib.parse import parse_qs


class TenantMiddleware(TenantMainMiddleware):
    
    @staticmethod
    def sapi_identify_tenant(request):
        try:
            team_id = str(parse_qs(request.body)[b'team_id'][0].decode('utf-8'))
            return team_id
        except:
            return "humhum"

    def tenant_id_from_request(self, request):
        if request.path.startswith("/t/"):
            tenant_id = request.path.lstrip("/t/").split("/")[0]
            return tenant_id
        elif request.path.startswith("/sapi/"):
            return self.sapi_identify_tenant(request)
        return ""

    def process_request(self, request):
        connection.set_schema_to_public()
        hostname_without_port = remove_www_and_dev(request.get_host().split(':')[0])
        tenant_id = self.tenant_id_from_request(request)

        try:
            # domain = get_tenant_domain_model() .objects.select_related('tenant').get(domain=hostname_without_port)
            domain = get_tenant_domain_model().objects.select_related('tenant').get(domain=tenant_id+'.'+hostname_without_port)
            # if (domain.tenant.active):
            #     request.tenant = domain.tenant
            #     request.urlconf = generate_tenant_url_module(domain.tenant)
            # else:
            #     request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
            
            request.tenant = domain.tenant
            request.urlconf = generate_tenant_url_module(domain.tenant)
        except utils.DatabaseError:
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
            return
        except get_tenant_domain_model().DoesNotExist:
            if hostname_without_port in (os.environ.get('SERVER_IP'), os.environ.get('SERVER_DOMAIN')):
                request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                return
            else:
                raise Http404

        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF

# class CustomMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         connection.set_schema_to_public()
#         hostname_without_port = remove_www_and_dev(request.get_host().split(':')[0])

#         try:
#             domain = get_tenant_domain_model().objects.select_related('tenant').get(domain=hostname_without_port)
#             request.tenant = domain.tenant
#         except utils.DatabaseError:
#             request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
#             return
#         except get_tenant_domain_model().DoesNotExist:
#             if hostname_without_port in (os.environ.get('SERVER_IP'), os.environ.get('SERVER_DOMAIN')):
#                 request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
#                 return
#             else:
#                 raise Http404

#         connection.set_tenant(request.tenant)
#         ContentType.objects.clear_cache()

#         if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
#             request.urlconf = settings.PUBLIC_SCHEMA_URLCONF



