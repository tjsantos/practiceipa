from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'practiceipa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^wordlists/', include('practice.urls', namespace='practice')),
    url(r'^', include('ipa.urls', namespace='ipa')),
)
# serve media files locally for development
# only works if DEBUG==True and MEDIA_URL is local (e.g. /media/)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
