from django.db import models
from django.contrib.auth.models import User
from random import shuffle

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    c1 = models.CharField(max_length=200,default='')
    c2 = models.CharField(max_length=200,default='')
    c3 = models.CharField(max_length=200,default='')
    c4 = models.CharField(max_length=200,default='')
    answer = models.CharField(max_length=200,default='c1')
 
    def __str__(self):
        return self.question_text

class Contestant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    current_que_id = models.IntegerField(default=1)
    first_login = models.BooleanField(default=False)
    que_array = models.TextField(default="",null=True)
    ans_array = models.TextField(default="",null=True)

    def __str__(self):
        return str(self.user)

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
        return [int(index) for index in self.que_array.split(" ")]

    def set_questions(self, question_list):
        shuffle(question_list)
        question_indexes_s = [str(element) for element in question_list]
        self.que_array = ' '.join(question_indexes_s)
        self.save()
# GETTERS ENDS
# ********************************************************

# SETTERS STARTS
# ======================================================= 
    def set_login(self, value):
        self.first_login = value
        self.save()

    def set_currqid(self, value):
        self.current_que_id = value
        self.save()
        
    def set_score(self, value):
        self.score = value
        self.save()

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
