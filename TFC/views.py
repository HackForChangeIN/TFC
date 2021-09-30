from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import CreateView,ListView
from TFC.models import *
from django.urls import reverse_lazy,reverse
from .forms import *
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate
import django.contrib.auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from ScreeningApp import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import uuid 
from django.core.mail import send_mail,EmailMessage
  

def subdomaincheck(request):
    request.subdomain = None
    host = request.META.get('HTTP_HOST', '')
    print(host)
    host_s = host.replace('www.', '').split('.')
    #print(host_s)
    if len(host_s) > 2:
        request.subdomain = ''.join(host_s[:-2])
        print(request.subdomain)
        if request.subdomain.endswith('staging' or 'dev'):
            request.subdomain = request.subdomain.replace('staging','')
    return request.subdomain
def admin_redirect(request):
    subdomain = subdomaincheck(request)
    print(subdomain , "redirected")
    if subdomain != None :
        if request.path.startswith(reverse('admin:index')):
            org = Organization.objects.get(subdomain = subdomain)
            return redirect('home')
    else:
        return redirect(reverse('admin:index')) 

def thanks(request):
    subdomain = subdomaincheck(request)
    org = Organization.objects.get(subdomain=subdomain)
    return render(request,'TFC/thanks.html',{'org':org})

def load_area_of_expertise(request):
    expertise_area_id = request.GET.get('profession')
    print(expertise_area_id)
    expertises = Expertise.objects.filter(category_of_expertise = expertise_area_id)
    print(expertises)
    return render(request,'TFC/areaofexpertise.html',{'expertises':expertises})

def screeninglink_mail(email,org,subdomain):
    volunteer = Candidate.objects.get(email = email)
    name = volunteer.name
    screening = Screenings.objects.create(candidate_id = volunteer)
    screeninguuid = screening.screening_uuid
    print(screeninguuid)
    email = volunteer.email
    from_email = settings.EMAIL_HOST_USER
    to = [email,]
    subject = "Screening Link"
    html_content = render_to_string('TFC/email.html', {'org': org,'subdomain':subdomain,'screeninguuid':screeninguuid,'name':name,'base_url':base_url})
    msg = EmailMessage(subject, html_content, from_email ,to)
    msg.content_subtype = "html"
    msg.send(fail_silently = True)
    print(" Screening Mail sended successfully")
    
def set_password_link(email,subdomain,org,auth_token,member_name):
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    subject = "Welcome Email"
    html_content = render_to_string('TFC/setpassword_link.html', {'org': org,'subdomain':subdomain,'auth_token':auth_token,'member_name':member_name})
    msg = EmailMessage(subject, html_content, from_email , [to])
    msg.content_subtype = "html"
    msg.send(fail_silently = True)
    print(" Password set email sended successfully")
    
class Home(View):
    def get(self, request):
        subdomain = subdomaincheck(request)
        #print(subdomain)
        if subdomain == None or subdomain == "" or subdomain == "dev":
            return render(request,'TFC/home.html')
        else:
            #subdomain=request.subdomain
            subdomain = subdomain.replace('dev', '')
            org=Organization.objects.get(subdomain=subdomain)
            return render(request,'TFC/orghome.html',{'org':org})
        
            
            
class OrganizationCreateView(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        if subdomain == None or subdomain == "" or subdomain=="dev":
            form1 = OrganizationSignupForm()
            form2 = MemberSignupForm()
            return render(request,'TFC/organization_signup.html',{'form1':form1,'form2':form2})
    def post(self,request):
        form1 = OrganizationSignupForm(request.POST,request.FILES)
        print(form1)
        form2 = MemberSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            email = form1.cleaned_data['email']
            member_email = form2.cleaned_data['member_email']
            if Organization.objects.filter(email = email).exists() or Team_Member.objects.filter(member_email = member_email).exists():
                messages.error(request,"Email already exist")
                return render(request,'TFC/organization_signup.html',{'form1':form1,'form2':form2})
            else:
                form1.save()
                org = Organization.objects.get(email = email)
                member = form2.save(commit = False)
                member.organization = org
                member.save()
                messages.success(request,"Organization Created Successfully")
                #password set link email
                auth_token = member.auth_token
                member_name = member.member_name
                subdomain = org.subdomain
                set_password_link(member_email,subdomain,org,auth_token,member_name)
                return redirect('organization_list')

    def get_success_url(self):
        return reverse('organization_list')

class OrganizationListView(ListView):
    def get(self,request):
         subdomain = subdomaincheck(request)
         if subdomain == None  or subdomain =="" or subdomain == "dev" :
             organization = Organization.objects.all()
             return render(request,'TFC/organization_list.html',{'organization':organization})

class PasswordSetView(View):
    form_class = TeamMemberSignupForm()
    def get(self,request,auth_token):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        fields = ['password','confirm_password']
        form = TeamMemberSignupForm()
        try:
            member = Team_Member.objects.get(auth_token = auth_token)
        except Team_Member.DoesNotExist:
            raise Http404("Your link has been expired")
        return render(request,"TFC/password_set.html",{'form':form,'org':org})
    
    def post(self,request,auth_token):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        form = TeamMemberSignupForm(request.POST)
        if form.is_valid():
            member = Team_Member.objects.get(auth_token = auth_token)
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
        try:
            if password == confirm_password :
                member.password = make_password(password)
                member.auth_token = None
                member.save()
                messages.success(request,"Password Created Successfully")
                return redirect('login')
            else:
                messages.error(request,"Please give the same password in Confirm Password")
                return render(request,"TFC/password_set.html",{'form':form,'org':org})
        except Team_Member.DoesNotExist:
            messages.error(request,"Password Not  Created")
            raise Http404("No  matches the given query.")

class ForgotPasswordView(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        return render(request,"TFC/password_reset.html",{'org':org})
    def post(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        if request.method == 'POST':
            email = request.POST['member_email']
            member = Team_Member.objects.get(member_email = email)
            if member.auth_token == None:
                member.auth_token = uuid.uuid4()
                auth_token = member.auth_token
                member_name = member.member_name
                print(auth_token)
                member.save()
                set_password_link(email,subdomain,org,auth_token,member_name)
                return render(request,"TFC/reset_pass_instruction.html",{'org':org})
            else:
                messages.error(request,"Please  activate your account by Setting Your Password from the link given in your mail")
                return redirect('login')

class LoginView(View):
    def get(self,request):
       subdomain = subdomaincheck(request)
       subdomain = subdomain.replace('dev', '')
       org = Organization.objects.get(subdomain=subdomain)
       form = LoginForm()
       fields = ['member_email','password']
       return render(request,"TFC/login.html",{'form':form,'org':org})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            subdomain = subdomaincheck(request)
            subdomain = subdomain.replace('dev', '')
            org = Organization.objects.get(subdomain = subdomain)
            member_email = form.cleaned_data['member_email']
            password = form.cleaned_data['password']
            member = Team_Member.objects.get(member_email = member_email)
            member_password = member.password
            match = check_password(password,member_password)
            if match and  org.name == member.organization.name:
                request.session['member'] = member.member_id
                print(request.session['member'])
                messages.success(request,"Successfully Log in to dashboard")
                return redirect('dashboard')
            else:
                messages.error(request,"Email or Password is wrong")
                return redirect('login')
                
class MemberCreateView(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            form = MemberCreateForm()
            return render(request,'TFC/member_signup.html',{'form':form,'org':org})
    def post(self,request):
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            subdomain = subdomaincheck(request)
            subdomain = subdomain.replace('dev', '')
            org = Organization.objects.get(subdomain = subdomain)
            member_name = form.cleaned_data['member_name']
            member_email = form.cleaned_data['member_email']
            member_phone_number = form.cleaned_data['member_phone_number']
            member=Team_Member(member_name = member_name,member_email = member_email,member_phone_number = member_phone_number,role = 'Member')
            member.organization = org
            member.save()
            auth_token = member.auth_token
            print(auth_token)
            set_password_link(member_email,subdomain,org,auth_token,member_name)
            messages.success(request,"Member Created Successfully")
            return redirect('team_member')
 
class MemberListView(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            return render(request,'TFC/members.html',{'org':org})

class MemberUpdate(View):
    def get(self,request,member_id):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            form = MemberCreateForm()
            member = Team_Member.objects.get(member_id = member_id)
            return render(request,'TFC/memberupdate.html',{'form':form,'org':org,'member':member})
    def post(self,request,member_id):
        member = Team_Member.objects.get(member_id = member_id)
        form = MemberCreateForm(request.POST,instance = member)
        if form.is_valid():
            form.save()
            messages.success(request,"Member Updated Successfully")
            return redirect ('team_member')

class MemberDelete(View):
    def get(self,request,member_id):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            member = Team_Member.objects.get(member_id = member_id)
            return render(request,'TFC/memberdelete.html',{'org':org,'member':member})
    def post(self,request,member_id):
        member = Team_Member.objects.get(member_id = member_id)
        member.delete()
        messages.success(request,"Member Deleted Successfully")
        return redirect ('team_member')

class OrgDashboard(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            print(member)
            member = Team_Member.objects.get(member_id = member)
            organization = member.organization.name
            print(member.organization.name)
            print(org.name)
            if org.name == member.organization.name:
                return render(request,'TFC/orgdashboard.html',{'org':org})
            else:
                return redirect('login')

def logout(request):
    auth_logout(request)
    messages.success(request,"Successfully Log out From your dashboard")
    return redirect('login')

class VolunteerCreateView(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain=subdomain)
        form = VolunteerForm()
        return render(request,'TFC/volunteer_signup.html',{'form':form,'org':org})
    def post(self,request):
        form = VolunteerForm(request.POST)
        print(request.POST)
        if form.is_valid():
            subdomain = subdomaincheck(request)
            org = Organization.objects.get(subdomain=subdomain)
            area_of_expertise = request.POST.getlist('area_of_expertise')
            vol = form.save(commit = False)
            vol.organization = org
            vol.save()
            form.save_m2m()
            email = vol.email
            try:
                screeninglink_mail(email,org,subdomain)
                print(vol.email)
            except:
                print('Error in sending email screening link to volunteer')
            messages.success(request,"Volunteer Registration Form Submitted Successfully")
            return redirect('thanks')

class VolunteerList(View):
    def get(self,request):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        member = request.session['member']
        screenings_list = []
        if member == None:
            return redirect('login')
        else:
            volunter = Volunteer.objects.filter(organization = org)
            return render(request,'TFC/volunter_list.html',{'org':org,'volunter':volunter})

class VolunteerDetails(View):
    def get(self,request,id):
        subdomain = subdomaincheck(request)
        subdomain = subdomain.replace('dev', '')
        org = Organization.objects.get(subdomain = subdomain)
        member = request.session['member']
        if member == None:
            return redirect('login')
        else:
            volunteer = Volunteer.objects.get(candidate_ptr_id = id)
            candidate = Candidate.objects.get(email = volunteer.email)
            screen_obj = Screenings.objects.filter(candidate_id = candidate).values('status','screening_result')
            print(screen_obj)
            return render(request,'TFC/volunteer_details.html',{'org':org,'volunteer':volunteer,'screen_obj':screen_obj})


 


            

