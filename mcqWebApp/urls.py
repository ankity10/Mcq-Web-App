"""mcqWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from questions import views
from registration.backends.default import urls


urlpatterns = [
    url(r'^ifdebug/', views.ifdebug, name='ifdebug'),
    url(r'^tests/(?P<test_id>\d+)/score/$', views.score, name='score'),
    url(r'^ans_submit/', views.ans_submit, name='ans_submit'),
    url(r'^q_submit/', views.state_change, name='q_submit'),
    url(r'^tests/(?P<test_id>\d+)/(?P<id>\d+)/$', views.question, name='contest_que'),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^tests/$', views.show_tests, name='tests'),
    url(r'^tests/(?P<test_id>\d+)/$', views.test_details, name='test_details'),
    url(r'^tests/(?P<test_id>\d+)/testcompleted/$', views.test_completed, name='test_completed'),
    url(r'^admin/', admin.site.urls),
]
