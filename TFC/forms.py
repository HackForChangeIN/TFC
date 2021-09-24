from django import forms
from django.forms import ModelForm
from .models import *
from ScreeningApp.models import *

class OrganizationSignupForm(ModelForm):
    
    class Meta:
        model=Organization
        fields=['name','website','partner_desc','phone_number','email','address' ,'city','state','zip_code',
        'upi_id','logo','focus_area']
        success_url = 'organization_list'
        
class MemberSignupForm(ModelForm):
    class Meta:
        model= Team_Member
        fields=[ 'member_name','member_email','member_phone_number','role']
        success_url='organization_list'

class TeamMemberSignupForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Team_Member
        fields=['password',]
        success_url='organization_list'
        widgets = {
            'password': forms.PasswordInput(),
        }
    confirm_password=forms.CharField(widget=forms.PasswordInput)



class LoginForm(ModelForm):
     password = forms.CharField(widget=forms.PasswordInput)
     class Meta:
         model=Team_Member
         fields=['member_email','password']
         widgets = {
            'password': forms.PasswordInput(),
        }
class VolunteerForm(ModelForm):
    field_order=['name','email','contact_number','dob','gender','highest_education','availability','current_occupation',
        'years_of_experience','profession','area_of_expertise']
    class Meta:
        model=Volunteer
        #fields=('__all__')
        exclude=('level_of_expertise','organization')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget=forms.RadioSelect(choices=GENDER)
        self.fields['highest_education'].widget=forms.RadioSelect(choices=EDUCATION)
        self.fields['availability'].widget=forms.RadioSelect(choices=AVAILABILITY)
        self.fields['current_occupation'].widget=forms.RadioSelect(choices=OCCUPATION)
        self.fields['years_of_experience'].widget=forms.RadioSelect(choices=EXPERIENCE)
        self.fields['area_of_expertise'].widget = forms.CheckboxSelectMultiple()
        self.fields['area_of_expertise'].queryset=Expertise.objects.none()
        if 'profession' in self.data:
            try:
                expertise_area_id = int(self.data.get('profession'))
                self.fields['area_of_expertise'].queryset =Expertise.objects.filter(category_of_expertise=expertise_area_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['area_of_expertise'].queryset = self.instance.expertise_area.expertise_set

class MemberCreateForm(ModelForm):
    class Meta:
        model=Team_Member
        fields=['member_name','member_email','member_phone_number']