from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<wordlist_id>\d+)/', include(patterns('',
        url(r'^$', views.wordlists, name='wordlists'),
        url(r'^(?P<wordlist_slug>[-\w]+)/$', views.wordlists, name='wordlists'),
    ))),
)
