from ScreeningApp.models import Question,Expertise_Area,Expertise
from faker import Faker
import random
faker = Faker()

category = ['management','engineering','masscom','marketing','administration']
expertise = {
				'management'    :  ['agile','sdlc','scrum','project management'],
				'engineering'   :  ['java','python','c++'],
				'masscom'       :  ['journalism','public relation','advertising','social media'],
				'marketing'     :  ['sales promotion','event marketing','digital media marketing','branding'],
				'administration':  ['zzz','xxx','yyy']
			}
level = ['entry level','intermediate','advanced','expert']


def produce_questions(n):
	for i in range(0,n):
		x = random.randint(0, len(category)-1)
		categ = category[x]
		exp = expertise[categ][random.randint(0, len(expertise[categ])-1)]
		lev = level[random.randint(0, len(level)-1)]
		qtype= 'multiple choice'
		r1 = random.randint(5,10)
		r2 = random.randint(5,20)
		topic = ''
		ques=''
		for i in range (0,r1):
			topic=topic+' '+faker.word()

		for i in range (0,r2):
			ques=ques+' '+faker.word()
		ques=ques+'?'
		option_1 = faker.word()
		option_2 = faker.word()
		option_3 = faker.word()
		option_4 = faker.word()
		options = [option_1,option_2,option_3,option_4]
		answer  = options[random.randint(0,3)]


		e  = Expertise_Area.objects.create(area_of_expertise = categ)
		f  = Expertise.objects.create(expertise = exp, category_of_expertise = e)
		q = Question.objects.create(category_of_expertise = e, expertise = f,
		 	level = lev, topic = topic , qtype = qtype , question = ques , 
		 	option_1 = option_1, option_2 = option_2 , option_3 = option_3 , 
		 	option_4 = option_4 , answer = answer)

produce_questions(20)
# print(ques)
# print(c)
# print(e)
# print(l)