from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<lang>\w+)/', include([
        url(r'^(?P<search>\w+)$', views.detail, name='detail'),
    ])),
    url(r'^search$', views.search, name='search')
]
