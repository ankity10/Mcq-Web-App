from django.db import models
from django.contrib.auth.models import User
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