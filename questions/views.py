# MODELS IMPORT 
# =======================================================
# import models from 'questions' app 
from .models import Question
from .models import Contestant

from django.contrib.auth.models import User


# Utility packages
# =======================================================
from random import shuffle
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# HELPER FUNCTIONS
# =======================================================

# Finds number of questions in database
def question_pk_list(request):
	try:
		pk = list(Question.objects.values_list("pk", flat=True))

	except ObjectDoesNotExist as err:
		return HttpError(request=request, error="Database Error: ObjectDoesNotExist", details=err)
	return pk

# Finds total number of questions
def total_questions(request):
	try:
		total = int(Question.objects.all().count())
	except ObjectDoesNotExist as err:
		return HttpError(request=request, error="Database Error: ObjectDoesNotExist", details=err)
	return total

# returns contestant for given user
def get_contestant(request):
	try:
		loggedin_user = User.objects.get(username=request.user)
		
	except ObjectDoesNotExist as err:
		return HttpError(request=request, error="Database Error: ObjectDoesNotExist", details=err)
		
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
		return HttpError(request=args['request'], error="Argument Error: function 'HttpError' requires 'error' and 'details' argument ", details="no details required")


# *******************************************************


# VIEWS SECTION STARTS
# =======================================================
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
	
	if contestant.first_login is False:
		# print("first login false")
		question_indexes = question_pk_list(request)
		print(question_indexes)
		shuffle(question_indexes)
		
		question_indexes_str = [str(index) for index in question_indexes]
		question_indexes_str = ' '.join(question_indexes_str)
		# updating answer array with dummy values as question primary keys
		Contestant.objects.filter(pk=contestant.id).update(ans_array=question_indexes_str)
		# updating question_array with the real indexes of questions from database
		Contestant.objects.filter(pk=contestant.id).update(que_array=question_indexes_str)
		
		Contestant.objects.filter(pk=contestant.id).update(first_login=True)
		id=1

	else:
		print("first login True")
		id = contestant.current_que_id

	return redirect('/contest/'+str(id))


# Contest_que view to present the question in front of user according to the url parameter id
@login_required
def question(request,id):
	contestant = get_contestant(request)

	question_indexes_s = contestant.que_array
	question_indexes_i = [int(i) for i in question_indexes_s.split(" ")]
	# question_id in url
	question_id = int(id)
	# if it is less than the number of questions in database
	if question_id <= total_questions(request):
		try:
			question_index = question_id - 1
			question_pk = question_indexes_i[question_index]
			print(question_pk)
		except IndexError as err:
			return HttpError(request=request, error="'question_array' List out of range!", details=err)

		try:
			question = Question.objects.get(pk=question_pk)
		except ObjectDoesNotExist as err:
			return HttpError(request=request, error="Database Error: ObjectDoesNotExist", details=err)
			
		context = {
		"question" : question,
		"id" : id,
		"title":"Question "+id+" | Welcome to mcqWebApp"
		}
		# redering the question ..success
		return render(request,'questions/question.html',context)
	
	# if primary key is not present	
	else:
		return HttpError(request=request, error="Question not found!", details="")


@login_required
def q_submit(request):
	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)

	if request.POST['type'] == 'next':
		if int(request.POST['cq']) <= contestant.current_que_id :
			cur_que = request.POST['cq']
			print(cur_que)
			Contestant.objects.filter(pk=contestant.id).update(current_que_id=int(cur_que)+1)
	else:
		cur_que = request.POST['cq']
		# print(cur_que)
		# usr = User.objects.get(username=request.user)
		# contestant = Contestant.objects.get(user=usr)
		# Contestant.objects.filter(pk=contestant.id).update(current_que_id=int(cur_que)-1)
	return HttpResponse("Succesfull ")


@login_required
def ans_submit(request):

	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)
	q_list = contestant.que_array
	q_list = [int(i) for i in q_list.split( )]
	cur_que_index = int(request.POST['cq'])-1
	cur_que = q_list[cur_que_index]
	question = Question.objects.get(pk=cur_que) #remove pk after changing questions dataset
	answer = request.POST['ans']
	if answer == question.answer:
		print("write answer")
		# Contestant.objects.filter(pk=contestant.id).update(score=contestant.score+4) #updating score
	else:
		print("wrong answer")

	str_ans_array = contestant.ans_array
	ans_array = str_ans_array.split(' ')
	ans_array[cur_que_index]=answer
	updated_str_ans_array = ' '.join(ans_array)
	Contestant.objects.filter(pk=contestant.id).update(ans_array=updated_str_ans_array)


	return HttpResponse("Succesfull")


@login_required
def score(request):
	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)
	# Contestant.objects.filter(pk=contestant.id).update(score=0) #updating score to 0
	
	q_list = contestant.que_array
	q_list = [int(i) for i in q_list.split( )]
	ans_array = contestant.ans_array
	ans_array = ans_array.split(' ')
	c_score = 0
	for i in range(contestant.current_que_id):
		contestant = Contestant.objects.get(user=usr)
		cur_que_index = i
		cur_que = q_list[cur_que_index]
		question = Question.objects.get(pk=cur_que) #remove pk after changing questions dataset
		answer = ans_array[i]
		if answer == question.answer:
			print("write answer")
			c_score = c_score + 4
	

	if contestant.score != c_score:
		Contestant.objects.filter(pk=contestant.id).update(score=c_score) #updating score

	context = {
	'score' : contestant.score,
	"title":"Score | Welcome to mcqWebApp"
	}

	return render(request,'questions/score.html',context)

# *******************************************************
