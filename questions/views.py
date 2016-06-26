# MODELS IMPORT 
# =======================================================
# import models from 'questions' app 
from .models import Question
from .models import Contestant

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
# Finds number of questions in database
def question_pk_list(request):
	try:
		pk = list(Question.objects.values_list("pk", flat=True))
	except ObjectDoesNotExist as err:
		return HttpError(request=request, 
			error="Database Error: ObjectDoesNotExist", 
			details=err)
	return pk

# Finds total number of questions
def total_questions(request):
	try:
		total = int(Question.objects.all().count())
	except ObjectDoesNotExist as err:
		return HttpError(request=request, 
			error="Database Error: ObjectDoesNotExist", 
			details=err)
	return total

# returns contestant for given user
def get_contestant(request):
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

# returns error
def HttpError(**args):
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
# Home page view 
def index(request):
	app_name = getattr(settings, "APP_NAME",None)
	context = {
	"title":"Home  | Welcome to mcqWebApp",
	"app_name":app_name
	}
	return render(request,'questions/index.html',context)


# Contest view ..first checks the current question state and then redirects to it
@login_required
def contest(request):
	contestant = get_contestant(request)
	# first time login
	if contestant.first_login is False:
		question_indexes = question_pk_list(request)
		contestant.set_questions(question_indexes)
		# updating answer array with dummy values as question primary keys
		contestant.set_answer(question_indexes)
		# updating question_array with the real indexes of questions from database
		contestant.set_login(True)
		id=1

	else:
		print("first login True")
		id = contestant.current_que_id
	return redirect('/contest/'+str(id))


# question view to present the question in front of user according to the url parameter id
@login_required
def question(request,id):
	contestant = get_contestant(request)
	question_indexes = contestant.get_questions()
	# question_id in url
	question_id = int(id)
	# if it is less than the number of questions in database
	if question_id <= total_questions(request):
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
		context = {
		"answer": answer,
		"question": question,
		"id": id,
		"title": "Question "+id+" | Welcome to mcqWebApp"
		}
		# redering the question ..success
		return render(request,'questions/question.html',context)
	
	# if primary key is not present	
	else:
		return HttpError(request=request, 
			error="Question not found!", 
			details="no details required")


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
	return HttpResponse("Succesfull")


@login_required
def score(request):
	contestant = get_contestant(request)
	# Contestant.objects.filter(pk=contestant.id).update(score=0) #updating score to 0
	
	question_indexes = contestant.get_questions()
	answer_array = contestant.get_answer_list()
	c_score = 0
	for i in range(total_questions(request)):
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

# VIEWS ENDS
# *******************************************************
