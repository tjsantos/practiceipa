from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'ipa.views.index', name='index'),
    url(r'^(?P<lang>\w+)/', include(patterns('',
        url(r'^(?P<search>\w+)$', 'ipa.views.detail', name='detail'),
    ))),
    url(r'^search$', 'ipa.views.search', name='search')
)
