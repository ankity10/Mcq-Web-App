from django.db import models
from django.contrib.auth.models import User
from random import shuffle

# Create your models here.


class Test(models.Model):

    test_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Question(models.Model):

    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    c1 = models.CharField(max_length=200, default='')
    c2 = models.CharField(max_length=200, default='')
    c3 = models.CharField(max_length=200, default='')
    c4 = models.CharField(max_length=200, default='')
    answer = models.CharField(max_length=200, default='c1')
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


class Association(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.test) + " ===> " + str(self.question)

    @classmethod
    def get_test_question_id(cls, test_id):
        association_obj = cls.objects.filter(test_id=test_id)
        question_id_list = [
            obj.question.question_id for obj in association_obj]
        return question_id_list


class Contestant(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ongoing_test = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def set_ongoing_test(self, test_id):
        self.ongoing_test = test_id
        self.save()

    def get_ongoing_test(self):
        return self.ongoing_test


class UsersTest(models.Model):

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    current_que_id = models.IntegerField(default=1)
    first_login = models.BooleanField(default=False)
    que_array = models.TextField(default="", null=True)
    ans_array = models.TextField(default="", null=True)
    test_progress = models.TextField(default="", null=True)
    test_submitted = models.IntegerField(default=0)

    def __str__(self):
        return str(self.test) + " ===> " + str(self.contestant)

    @classmethod
    def get_user_tests(cls, contestant_id):
        user_test_objs = UsersTest.objects.filter(contestant_id=contestant_id)
        return [objs.test for objs in user_test_objs]


# GETTERS START
# =======================================================
    def get_answer(self, index):
        value = self.ans_array.split(" ")[index]
        return value

    def get_answer_list(self):
        return self.ans_array.split(" ")

    def set_answer(self, answers):
        self.ans_array = answers
        self.save()

    def get_questions(self):
        question_list = []
        for id in [int(index) for index in self.que_array.split(" ")]:
            question_list.append(Question.objects.get(pk=id))
        return question_list

    def set_questions(self, question_list):
        shuffle(question_list)
        question_indexes_s = [str(element) for element in question_list]
        self.que_array = ' '.join(question_indexes_s)
        self.save()

    def get_question_indices(self):
        return [int(index) for index in self.que_array.split(" ")]

    def get_curr_qid(self):
        return self.current_que_id

    def get_test_submitted(self):
        return self.test_submitted

# GETTERS ENDS
# ********************************************************

# SETTERS STARTS
# =======================================================
    def set_login(self, value):
        self.first_login = value
        self.save()

    def set_curr_qid(self, value):
        self.current_que_id = value
        self.save()

    def set_score(self, value):
        self.score = value
        self.save()

    def set_test_submitted(self):
        self.test_submitted = 1
        self.save

# SETTERS ENDS
# ********************************************************

# UPDATE STARTS
# =======================================================
    def update_answer(self, index, value):
        self.ans_array = self.ans_array.split(" ")
        self.ans_array[index] = value
        self.ans_array = ' '.join(self.ans_array)
        self.save()
# UPDATE ENDS
# *******************************************************
