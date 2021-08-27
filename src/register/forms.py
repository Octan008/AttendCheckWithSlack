from django import forms
from .models import Tenants


# class GenerateUsersForm(forms.Form):
#     pass

class GenerateUsersForm(forms.Form):
    team_name = forms.CharField(
        label='SlackTeam',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    team_code = forms.CharField(
        label='ID',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    # def register(self):
    #     Tenants.objects.all().delete();
    #     tnts = Tenants(name = self.form_class.team_name, code = self.form_class.team_code )
    #     tnts.save()

