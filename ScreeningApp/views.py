from django.shortcuts import render, redirect
from .models import *
import json
import itertools
from .import forms
from TFC.models import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.conf import settings
import uuid
#from HFCCore.models import Community_Member
from django.views import View
from django.core.mail import send_mail
# Create your views here.
def screening_result(email,name,screening_status):
    #from_email=settings.EMAIL_HOST_USER
	from_email = 'HackForChange Team<noreply@hackforchange.co.in>'
	to = [email,]
	subject = "Screening Result"
	headers = {'Reply-To': 'suman@hackforchange.co.in'}
	html_content = render_to_string('HFC/screen_result_email.html', {'name':name,'screening_status':screening_status})
	msg = EmailMessage(subject, html_content, from_email ,to,headers = headers)
	msg.content_subtype = "html"
	msg.send(fail_silently = True)
	print("Mail sended successfully")  

class Screening(View):
	def get(self,request,screening_uuid):
		mentors = Community_Member.objects.filter(type = 'Mentor')[:6]
		screen = Screenings.objects.get(screening_uuid = screening_uuid)
		if screen.status == 'Passed' or screen.status == 'Failed':
			return redirect('screening-status',screening_uuid)
		if screen.status == "Closed":
			return render(request, 'ScreeningApp/screening_error.html')
		screening_id = screen.screening_id
		questions = Screenings_Questions.objects.filter(screening_id = screening_id)
		return render(request, 'ScreeningApp/screening.html', {'questions': questions, 'screening_uuid': screening_uuid,'mentors':mentors})
	def post(self,request,screening_uuid):
		data = request.POST.dict()
		if 'csrfmiddlewaretoken' in data:
    			del data['csrfmiddlewaretoken']
		for qid,ans in data.items():
			obj = Screenings_Questions.objects.get(pk = qid)
			obj.candidate_ans = ans
			obj.save()
		print(obj.screening_id)
		return redirect('screening_preview', screening_uuid)

class Screening_Preview(View):
	def get(self,request,screening_uuid):
		mentors = Community_Member.objects.filter(type = 'Mentor')[:6]
		screen = Screenings.objects.get(screening_uuid = screening_uuid)
		if screen.status == 'Passed' or screen.status == 'Failed':
			return render(request, 'ScreeningApp/screening_completed.html')
		screening_id = screen.screening_id
		questions = Screenings_Questions.objects.filter(screening_id=screening_id)
		return render(request, 'ScreeningApp/screening_submission.html', {'questions': questions,'mentors':mentors})
	def post(self,request,screening_uuid):
		data = request.POST.dict()
		if 'csrfmiddlewaretoken' in data:
			del data['csrfmiddlewaretoken']
		true_count = false_count = 0
		for qid,ans in data.items():
			obj = Screenings_Questions.objects.get(pk = qid)
			if (obj.correct_ans == obj.candidate_ans):
				obj.answer_correctness = True
				obj.save()
				true_count = true_count+1
				print(obj.answer_correctness)
			else:
				obj.answer_correctness = False
				obj.save()
				print(obj.answer_correctness)
				false_count = false_count + 1
		total = true_count + false_count
		percentage = int((true_count / total) * 100)
		screeningid = obj.screening_id.screening_id
		if (percentage >= 70):
			screening_obj = Screenings.objects.filter(screening_id = screeningid).update(status = 'Passed')
			screening_obj = Screenings.objects.filter(screening_id = screeningid).update(screening_result = percentage)
			screen_obj = Screenings.objects.get(screening_id = screeningid)
			cand_id = screen_obj.candidate_id.candidate_id
			candidate_obj = Candidate.objects.get(candidate_id = cand_id)
			name = candidate_obj.name
			screening_status = screen_obj.status
			return redirect('result',screening_uuid)
		else:
			screening_obj = Screenings.objects.filter(screening_id = screeningid).update(status = 'Failed')
			screening_obj = Screenings.objects.filter(screening_id = screeningid).update(screening_result = percentage)
			screen_obj = Screenings.objects.get(screening_id = screeningid)
			cand_id = screen_obj.candidate_id.candidate_id
			candidate_obj = Candidate.objects.get(candidate_id = cand_id)
			name = candidate_obj.name
			screening_status = screen_obj.status
			return redirect('result',screening_uuid)

class Result(View):
	def get(self,request,screening_uuid):
		screen_obj = Screenings.objects.get(screening_uuid = screening_uuid)
		candidate_name =  screen_obj.candidate_id
		
		percentage = screen_obj.screening_result
		if screen_obj.status == 'Passed':
			message = "{name} passed the screening with  {percentage} percentage".format(name = candidate_name, percentage = percentage)
			to_list = ['team@hackforchange.co.in',]
			send_mail('Screening Result', message,'HackForChange Team<noreply@hackforchange.co.in>',to_list)
			return render(request, 'ScreeningApp/screening_result_pass.html')
		if screen_obj.status == 'Failed':
			return render(request, 'ScreeningApp/screening_result_fail.html')

class Feedback(View):
	def get(self,request,screening_uuid):
		screen = Screenings.objects.get(screening_uuid = screening_uuid)
		if screen.status == 'Open':
    			return redirect('screening',screening_uuid)
		mentors = Community_Member.objects.filter(type = 'Mentor')[:6]
		screening_id = screen.screening_id
		questions = Screenings_Questions.objects.filter(screening_id=screening_id)
		return render(request, 'ScreeningApp/screening_feedback.html', {'questions': questions, 'Screeninguuid':screening_uuid,'screen':screen,'mentors':mentors})
