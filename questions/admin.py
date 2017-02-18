from django.contrib import admin

from .models import Question, Contestant, Test, Association, UsersTest
# Register your models here.
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Contestant)
admin.site.register(Association)
admin.site.register(UsersTest)
