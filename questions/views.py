# MODELS IMPORT 
# =======================================================
# import models from 'questions' app 
from .models import Question
from .models import Contestant
from .models import Test
from .models import Association
from .models import UserTest
from django.contrib.auth.models import User

# UTILITY PACKAGES
# =======================================================
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# HELPER FUNCTIONS START
# =======================================================
def question_pk_list(request):
	'''
	Finds number of questions in database
	'''
	try:
		pk_list = list(Question.objects.values_list("pk", flat=True))
	except ObjectDoesNotExist as err:
		return HttpError(request=request, 
						 error="Database Error: ObjectDoesNotExist", 
						 details=err)
	return pk_list

def total_questions(request):
	'''
	Finds total number of questions
	'''
	try:
		total = int(Question.objects.all().count())
	except ObjectDoesNotExist as err:
		return HttpError(request=request, 
						 error="Database Error: ObjectDoesNotExist", 
						 details=err)
	return total

def get_contestant(request):
	'''
	returns contestant for given user
	'''
	try:
		loggedin_user = User.objects.get(username=request.user)
	except ObjectDoesNotExist as err:
		return HttpError(request=request, 
						 error="Database Error: ObjectDoesNotExist", 
						 details=err)
	try:
		contestant = Contestant.objects.get(user=loggedin_user)
	# if user logins for first time	set the contestant with user
	except ObjectDoesNotExist:
		contestant = Contestant(user=loggedin_user)
		contestant.save()
	return contestant

def HttpError(**args):
	'''
	Error wrapper
	'''
	if args['error'] and args['details'] and args['request']:
		error = args['error']
		details = args['details']
		try:
			title = args['title']
		except KeyError:
			title = "Error | mcqWebApp"
		context = {
		"error": error,
		"title": title
		}	
		return render(args['request'], 'questions/error.html',context)
	else:
		return HttpError(request=args['request'], 
						 error="Argument Error: function 'HttpError' requires 'error' and 'details' argument ", 
						 details="no details required")

# HELPER FUNCTIONS ENDS
# *******************************************************

# VIEWS STARTS
# =======================================================
def index(request):
	'''
	Home page view 
	'''
	app_name = getattr(settings, "APP_NAME",None)
	context = {
	"title":"Home  | Welcome to mcqWebApp",
	"app_name":app_name
	}
	return render(request,'questions/index.html',context)

@login_required
def contest(request,id):
	'''
	Contest view ..first checks the current question state and then redirects to it
	'''
	contestant = get_contestant(request)
	# first time login
	id = 4
	if contestant.first_login is False:
		question_indexes = test_details(request, id)
		contestant.set_questions(question_indexes)
		contestant.set_answer(question_indexes)
		contestant.set_login(True)
		id=1
	else:
		print("first login True")
		id = contestant.current_que_id
	return redirect('/test/'+str(id))

@login_required
def score(request):
	contestant = get_contestant(request)
	question_indexes = contestant.get_question_indices()
	answer_array = contestant.get_answer_list()
	c_score = 0
	total_ques = len(question_indexes)
	for i in range(total_ques):
		cur_que_index = i
		cur_que = question_indexes[cur_que_index]
		question = Question.objects.get(pk=cur_que)
		answer = answer_array[i]
		if answer == question.answer:
			print("write answer")
			c_score = c_score + 4
	contestant.set_score(c_score)
	context = {
	'score' : contestant.score,
	"title":"Score | Welcome to mcqWebApp"
	}
	return render(request,'questions/score.html',context)

def ifdebug(request):
	debug = getattr(settings, "DEBUG", None)
	return HttpResponse(debug)

@login_required
def question(request,id,test_id):
	'''
	question view to present the question in front of user according to the url parameter id
	'''
	contestant = get_contestant(request)
	question_indexes = contestant.get_question_indices()
	total = total_questions(request)
	# question_id in url
	question_id = int(id)
	total_ques = len(contestant.get_question_indices())
	if question_id <= total_ques:
		try:
			question_num = question_id - 1
			question_pk = question_indexes[question_num]
		except IndexError as err:
			return HttpError(request=request, 
							 error="'question_array' List out of range!", 
							 details=err)
		try:
			question = Question.objects.get(pk=question_pk)
		except ObjectDoesNotExist as err:
			return HttpError(request=request, 
							 error="Database Error: ObjectDoesNotExist", 
							 details=err)
		answer = contestant.get_answer(question_num)
		contestant.set_currqid(id)
		context = {
		"answer": answer,
		"question": question,
		"id": id,
		"test_id":test_id,
		"total":total,
		"title": "Question "+id+" | Welcome to mcqWebApp"
		}
		return render(request,'questions/question.html',context)
	else:
#		return HttpError(request=request, 
#						 error="Question not found!", 
#						 details="no details required")
		return redirect ('/score/') 

@login_required
def state_change(request):
	contestant = get_contestant(request)
	cur_que = request.POST['cq']
	# if user clicks next button
	if request.POST['type'] == 'next':
		if int(cur_que) <= contestant.current_que_id :
			contestant.set_currqid(int(cur_que)+1)
	# if user clicks previous button
	else:
		contestant.set_currqid(int(cur_que)-1)
	return HttpResponse("Succesfull ")

@login_required
def ans_submit(request):
	contestant = get_contestant(request)
	question_indexes = contestant.get_questions()
	cur_question_num = int(request.POST['cq'])-1
	cur_question = question_indexes[cur_question_num]
	question = Question.objects.get(pk=cur_question)
	answer = request.POST['ans']
	contestant.update_answer(cur_question_num, answer)
	return HttpResponse("Successful")



# added by shrunoti
@login_required
def get_tests(request):
	contestant = get_contestant(request)
	tests = UserTest.get_user_tests(contestant.id)
	return render (request, 'questions/tests.html', {'tests':tests}) 

@login_required	
def test_details(request,id):
	asso_objs = Association.objects.filter(test_id = id)
	#questions = [objs.question for objs in asso_objs]
	# q_str_list = [str(question.question_id) for question in questions]
	contestant = get_contestant(request)
	
	if contestant.first_login is False:
		
		contestant.set_questions(q_str_list)
		contestant.set_answer(q_str_list)
		questions = contestant.get_questions()
		contestant.set_login(True)
	
	else:
		questions = contestant.get_questions

	
	context = {
	'questions' : questions,
	'test_id': id
	
	}
	return render (request, 'questions/test_details.html', context)
	# return HttpResponse(q_ids)

# def get_question_id_list(id):
# 	question_id_list = Association.get_test_question_id(id)
# 	q_str_list = [ str(q_id) for q_id in question_id_list ]
# 	q_str = " ".join(q_str_list)
# 	return HttpResponse(q_str)












# VIEWS ENDS
# *******************************************************
