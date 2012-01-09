from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('registrationApp.views',
    url(r'^registrationApp/$', 'index'),
    url(r'^registrationApp/$', 'detail'),
    url(r'^registrationApp/search/$', 'search'),
    url(r'^registrationApp/searchResults/$', 'searchResults'),
)
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)