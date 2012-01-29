from django.conf.urls.defaults import patterns, include, url
from registrationApp.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('registrationApp.views',
    url(r'^registrationApp/$', 'index', name = 'index'),    
    url(r'^registrationApp/loginView/$', 'loginView'),
    url(r'^registrationApp/(?P<Student_id>\d+)/search/$', 'search', name = 'search'),
    url(r'^registrationApp/(?P<Student_id>\d+)/searchResults/$', 'searchResults', name = 'searchResults'),
    url(r'^registrationApp/(?P<Student_id>\d+)/add/$', 'add', name = 'add'),
    url(r'^registrationApp/(?P<Student_id>\d+)/delete/$', 'delete', name = 'delete'),
    url(r'^registrationApp/(?P<Student_id>\d+)/one/$', 'one', name = 'one'),

)
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),

)