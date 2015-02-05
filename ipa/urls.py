from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'ipa.views.index', name='index'),
    url(r'^(\w+)/(\w+)$', 'ipa.views.detail', name='detail'),
    url(r'^search$', 'ipa.views.search', name='search')
)
