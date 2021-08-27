from django.shortcuts import render

from django.contrib.auth.models import User
from .models import Tenants
from django.db.utils import DatabaseError
from django.views.generic import FormView, TemplateView, CreateView
from .forms import GenerateUsersForm
# from . import forms
from tenants.models import Client, Domain
from random import choice
# from tenant_only.models import UploadFile

from django_tenants.urlresolvers import reverse_lazy

import os

class TenantView(TemplateView):
    template_name = "index_tenant.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenants_list'] = Client.objects.all()
        return context


class TenantViewRandomForm(FormView):
    form_class = GenerateUsersForm
    template_name = "random_form.html"
    success_url = reverse_lazy('random_form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenants_list'] = Client.objects.all()
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):   
        try:
            Client.objects.all().delete();
            Domain.objects.all().delete();

            tenant = Client(schema_name='public',
                            name='public',
                            paid_until='2016-12-05',
                            on_trial=False)
            tenant.save()

            # Add one or more domains for the tenant
            domain = Domain()
            domain.domain = os.environ.get('SERVER_DOMAIN') # don't add your port or www here! on a local server you'll want to use localhost here
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            # create your public tenant
            tenant2 = Client(schema_name=self.request.POST['team_code'],
                            name=self.request.POST['team_name'],
                            paid_until='2016-12-05',
                            on_trial=False)
            tenant2.save()

            # Add one or more domains for the tenant
            domain2 = Domain()
            domain2.domain = self.request.POST['team_code']+'.'+os.environ.get('SERVER_DOMAIN') # don't add your port or www here! on a local server you'll want to use localhost here
            domain2.tenant = tenant2
            domain2.is_primary = True
            domain2.save()

            tenant3 = Client(schema_name="dummy",
                name="dummy",
                paid_until='2016-12-05',
                on_trial=False)
            tenant3.save()

            # Add one or more domains for the tenant
            domain3 = Domain()
            domain3.domain = "dummy"+'.'+os.environ.get('SERVER_DOMAIN') # don't add your port or www here! on a local server you'll want to use localhost here
            domain3.tenant = tenant3
            domain3.is_primary = True
            domain3.save()
            
            
        except DatabaseError:
            pass

        # return super().form_valid(form)
        return render(self.request, 'user_data_confirm.html', {'form': form})


# class TenantViewFileUploadCreate(CreateView):
#     template_name = "upload_file.html"
#     model = UploadFile
#     fields = ['filename']
#     success_url = reverse_lazy('upload_file')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tenants_list'] = Client.objects.all()
#         context['upload_files'] = UploadFile.objects.all()
#         return context



# Create your views here.
