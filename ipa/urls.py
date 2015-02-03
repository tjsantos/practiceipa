from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'ipa.views.index', name='index')
)
