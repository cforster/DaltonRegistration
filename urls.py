from django.conf.urls.defaults import patterns, include, url
from registrationApp.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('registrationApp.views',
    url(r'^registrationApp/$', 'index', name = 'index'),    
    url(r'^registrationApp/search/$', 'search', name = 'search'),
    url(r'^registrationApp/searchResults/$', 'searchResults', name = 'searchResults'),
    url(r'^registrationApp/add/$', 'add', name = 'add'),
    url(r'^registrationApp/addEnrolledSection/$', 'addEnrolledSection', name = 'addEnrolledSection'),
    url(r'^registrationApp/delete/$', 'delete', name = 'delete'),
    url(r'^registrationApp/one/$', 'one', name = 'one'),
    url(r'^registrationApp/schedule/$', 'schedule', name = 'schedule'),
    url(r'^registrationApp/submit/$', 'submit', name = 'submit'),
    url(r'^registrationApp/(?P<DepartmentChair_id>\d+)/preapprovals/$', 'preapprovals', name = 'preapprovals'),
    url(r'^registrationApp/(?P<DepartmentChair_id>\d+)/preAppContainer/$', 'preAppContainer', name = 'preAppContainer'),
    url(r'^registrationApp/(?P<DepartmentChair_id>\d+)/preAppAdd/$', 'preAppAdd', name = 'preAppAdd'),
    url(r'^registrationApp/(?P<House_id>\d+)/advisor/$', 'advisor', name = 'advisor'),
    url(r'^registrationApp/(?P<House_id>\d+)/approve/$', 'approve', name = 'approve'),
    url(r'^registrationApp/(?P<House_id>\d+)/review/$', 'review', name = 'review'),

)
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
	url(r'^registrationApp/login/$', 'django.contrib.auth.views.login', {'template_name': 'registrationApp/login.html'}, name='login'),
    url(r'^registrationApp/logout/$', 'django.contrib.auth.views.logout',{'template_name': 'registrationApp/logout.html'}),    
)