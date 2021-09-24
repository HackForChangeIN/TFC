from django.contrib import admin
from .models import *

class Team_MemberInline(admin.TabularInline):
	model = Team_Member
	list_display =('member_name','member_email','member_phone_number','role')
	
	exclude=['password',]
	extra=0
	list_display_links = ('member_name',)
	readonly_fields=('auth_token',)
	
	
	
	

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name','website','partner_desc','phone_number','email','logo','address','city','state','zip_code','focus_area','subdomain','thankyou_template','upi_id')
	inlines =[Team_MemberInline]
	class meta:
		model=Organization
admin.site.register(Organization,OrganizationAdmin)


class Team_MemberAdmin(admin.ModelAdmin):
	#readonly_fields=('organization',)
	list_display=('member_name','member_email','member_phone_number','role','organization')
	
	exclude=['password',]
	class meta:
		model=Team_Member
admin.site.register(Team_Member,Team_MemberAdmin)

class VolunteerAdmin(admin.ModelAdmin):
	list_display=('organization','name','email','contact_number','dob','gender','highest_education','availability','current_occupation','years_of_experience','profession','areaofexpertise')
	exclude=['level_of_expertise']
	class meta:
		model=Volunteer
admin.site.register(Volunteer,VolunteerAdmin)