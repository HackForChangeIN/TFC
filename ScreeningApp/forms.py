from ScreeningApp.models import *
from django import forms
from django.forms.widgets import RadioSelect

class QuestionForm(forms.Form):
    def __init__(self,  *args, **kwargs):
        self.screening_id = kwargs.pop('screening_id')
        super(QuestionForm, self).__init__(*args, **kwargs)
        #choice_list = [x for x in question.get_questions()]
        questions = Screenings_Questions.objects.filter(screening_id = self.screening_id)
        choice_list=[]
        for question in questions:
            for item in question.question.all():
                pass
        choice_list=[item.option_1 for item in question.question.all() for question in questions]
        