from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<wordlist_id>\d+)/', include([
        url(r'^$', views.wordlists, name='wordlists'),
        url(r'^(?P<wordlist_slug>[-\w]+)/', include([
            url(r'^$', views.wordlists, name='wordlists'),
            url(r'^(?P<page>\d+)/$', views.wordlists, name='wordlists'),
            url(r'^quiz/$', views.quiz, name='quiz'),
            url(r'^quiz/(?P<q_id>\d+)/$', views.quiz_question, name='quiz_question'),
            url(r'^reset/$', views.reset_progress, name='reset_progress'),
        ]))
    ])),
]
