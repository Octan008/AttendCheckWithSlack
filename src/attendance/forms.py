from django import forms
# from .models import Tenants
from .models import AttendLog

import bootstrap_datepicker_plus as datetimepicker


# class GenerateUsersForm(forms.Form):
#     pass

class GenerateValidForm(forms.Form):
    hook_url = forms.CharField(
        label='hook_url',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    # team_code = forms.CharField(
    #     label='ID',
    #     max_length=20,
    #     required=True,
    #     widget=forms.TextInput()
    # )
    # def register(self):
    #     Tenants.objects.all().delete();
    #     tnts = Tenants(name = self.form_class.team_name, code = self.form_class.team_code )
    #     tnts.save()

# class LogEditForm(forms.ModelForm):
    
#     class Meta:
        # def __init__(self, *args, **kwargs):
        #     super(ItemForm, self).__init__(*args, **kwargs)
        #     self.fields['price']= forms.IntegerField(min_value=1)

        # model = AttendLog
        # fields = ('login_time', 'logout_time')
        # widgets = {
        #     'login_time': datetimepicker.DateTimePickerInput(
        #         format='%Y-%m-%d %H:%M:%S',
        #         options={
        #             'locale': 'ja',
        #             'dayViewHeaderFormat': 'YYYY年 MMMM',
        #         }
        #     ),

        #     'logout_time': datetimepicker.DateTimePickerInput(
        #         format='%Y-%m-%d %H:%M:%S',
        #         options={
        #             'locale': 'ja',
        #             'dayViewHeaderFormat': 'YYYY年 MMMM',
        #         }
        #     )
        # }

class LogEditForm(forms.Form):
    ids=forms.CharField(
        max_length=100,
        required=True,
        widget=forms.HiddenInput()
    )

# def CreateLogEditForm(records, *arg):
#     f = LogEditForm(*arg)
#     for record in records:


#     date = forms.DateField(
#     widget=datetimepicker.DateTimePickerInput(
#             format='%Y-%m-%d %H:%M:%S',
#             options={
#                 'locale': 'ja',
#                 'dayViewHeaderFormat': 'YYYY年 MMMM',
#             }
#         ),
#     required=True
# )
def AddLogEditFields(f ,record):
    # f.fields['id'+str(record.id)]=forms.IntegerField(
    #     initial=record.id, 
    #     widget=forms.HiddenInput(),
    #     required=True
    #     )
    f.fields['login_time'+str(record.id)]=forms.DateTimeField(
        initial=record.login_time, 
        required=True,
         widget=datetimepicker.DateTimePickerInput(
            format='%Y-%m-%d %H:%M:%S',
            options={
                'locale': 'ja',
                'dayViewHeaderFormat': 'YYYY年 MMMM',
            }
        )
    )
    f.fields['logout_time'+str(record.id)]=forms.DateTimeField(
        initial=record.logout_time, 
        required=True,
        widget=datetimepicker.DateTimePickerInput(
            format='%Y-%m-%d %H:%M:%S',
            options={
                'locale': 'ja',
                'dayViewHeaderFormat': 'YYYY年 MMMM',
            }
        )
    )
    return f
    



class LogForm(forms.Form):
    class Meta:
        pass

