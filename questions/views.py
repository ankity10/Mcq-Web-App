# MODELS IMPORT
# =======================================================
# import models from 'questions' app
from .models import Question
from .models import Contestant
from .models import Test
from .models import Association
from .models import UsersTest
from django.contrib.auth.models import User

# UTILITY PACKAGES
# =======================================================
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render, redirect
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
        return render(args['request'], 'questions/error.html', context)
    else:
        return HttpError(
            request=args['request'],
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
    app_name = getattr(settings, "APP_NAME", None)
    context = {
        "title": "Home  | Welcome to mcqWebApp",
        "app_name": app_name
    }
    return render(request, 'questions/index.html', context)


@login_required
def score(request, test_id):
    userstest = get_user_tests(request, test_id)
    question_indexes = userstest.get_question_indices()
    answer_array = userstest.get_answer_list()
    c_score = 0
    total_ques = len(question_indexes)
    for i in range(total_ques):
        cur_que_index = i
        cur_que = question_indexes[cur_que_index]
        question = Question.objects.get(pk=cur_que)
        question_score = question.marks
        answer = answer_array[i]
        if answer == question.answer:
            print("write answer")
            c_score = c_score + question_score
    userstest.set_score(c_score)
    context = {
        'score': userstest.score,
        "title": "Score | Welcome to mcqWebApp"
    }
    return render(request, 'questions/score.html', context)


def ifdebug(request):
    debug = getattr(settings, "DEBUG", None)
    return HttpResponse(debug)


@login_required
def question(request, id, test_id):
    '''
    question view to present the question in front of user according to the url parameter id
    '''
    userstest = get_user_tests(request, test_id)
    question_indexes = userstest.get_question_indices()
    question_id = int(id)
    total_ques = len(userstest.get_question_indices())
    if question_id <= total_ques + 1:
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
        answer = userstest.get_answer(question_num)
        userstest.set_curr_qid(id)
        context = {
            "answer": answer,
            "question": question,
            "id": id,
            "test_id": test_id,
            "total": total_ques,
            "title": "Question " + id + " | Welcome to mcqWebApp"
        }
        test_submitted = userstest.get_test_submitted()
        if test_submitted:
            return render(request, 'questions/test_submitted.html')
        else:
            return render(request, 'questions/question.html', context)


@login_required
def state_change(request):
    contestant = get_contestant(request)
    test_id = contestant.get_ongoing_test()
    userstest = get_user_tests(request, test_id)
    cur_que = userstest.get_curr_qid()
    # if user clicks next button
    if request.POST['type'] == 'next':
        if int(cur_que) <= userstest.current_que_id:
            userstest.set_curr_qid(int(cur_que) + 1)
    # if user clicks previous button
    else:
        userstest.set_curr_qid(int(cur_que) - 1)
    return HttpResponse("Succesfull ")


@login_required
def ans_submit(request):
    contestant = get_contestant(request)
    test_id = contestant.get_ongoing_test()
    userstest = get_user_tests(request, test_id)
    question_indexes = userstest.get_question_indices()
    cur_question_num = (userstest.get_curr_qid()) - 1
    cur_question = question_indexes[cur_question_num]
    question = Question.objects.get(pk=cur_question)
    answer = request.POST['ans']
    userstest.update_answer(cur_question_num, answer)
    return HttpResponse("Successful")


# added by shrunoti
def get_tests(request, contestant):
    tests = UsersTest.get_user_tests(contestant.id)
    return tests


def get_user_tests(request, test_id):
    contestant = get_contestant(request)
    userstest = UsersTest.objects.get(contestant=contestant, test_id=test_id)
    return userstest


@login_required
def show_tests(request):
    contestant = get_contestant(request)
    tests = get_tests(request, contestant)
    return render(request, 'questions/tests.html', {'tests': tests})


@login_required
def test_details(request, test_id):
    contestant = get_contestant(request)
    contestant.set_ongoing_test(test_id)
    userstest = get_user_tests(request, test_id)
    asso_objs = Association.objects.filter(test_id=test_id)
    questions = [objs.question for objs in asso_objs]
    q_str_list = [str(question.question_id) for question in questions]

    if userstest.first_login is False:
        curr_id = userstest.get_curr_id()
    else:
        curr_id = 1
    # contestant = get_contestant(request)

    if userstest.first_login is False:

        userstest.set_questions(q_str_list)
        userstest.set_answer(q_str_list)
        questions = userstest.get_questions()
        userstest.set_login(True)
    else:
        questions = userstest.get_questions
    context = {
        'questions': questions,
        'test_id': test_id,
        'curr_id': curr_id
    }
    return render(request, 'questions/test_details.html', context)


@login_required
def test_completed(request, test_id):
    userstest = get_user_tests(request, test_id)
    userstest.set_test_submitted()
    return render(request,
                  'questions/test_completed.html',
                  {'test_id': test_id})

# VIEWS ENDS
# *******************************************************
