from django.conf.urls.defaults import patterns, include, url
from registrationApp.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('registrationApp.views',
    url(r'^$', 'index', name = 'index'),    
    url(r'^searchResults/$', 'searchResults', name = 'searchResults'),
    url(r'^add/$' , 'add', name = 'add'),
    url(r'^delete/$', 'delete', name = 'delete'),
    url(r'^one/$', 'one', name = 'one'),
    url(r'^catalog/$', 'catalog', name = 'catalog'), 
    url(r'^schedule/$', 'schedule', name = 'schedule'),
    url(r'^preferences/$', 'preferences', name = 'preferences'),
    url(r'^submit/$', 'submit', name = 'submit'),
    url(r'^notifications/$', 'notifications', name = 'notifications'),
    url(r'^notifRead/$', 'notifRead', name = 'notifRead'),
    url(r'^rankChange/$', 'rankChange', name = 'rankChange'),
    url(r'^alternate/$', 'alternate', name = 'alternate'),
    url(r'^warningOutput/$', 'warningOutput', name = 'warningOutput'),
    url(r'^studentSchedule/$', 'studentSchedule', name = 'studentSchedule'),
    
    url(r'^preapprovals/$', 'preapprovals', name = 'preapprovals'),
    url(r'^preappContainer/$', 'preappContainer', name = 'preappContainer'),
    url(r'^preappAdd/$', 'preappAdd', name = 'preappAdd'),
    
    url(r'^advisor/$', 'advisor', name = 'advisor'),
    url(r'^approve/$', 'approve', name = 'approve'),
    url(r'^review/$', 'review', name = 'review'),

    url(r'^test/$', 'test', name = 'test'),
    url(r'^printSchedule/$', 'printSchedule', name = 'printSchedule'),


    url(r'^ParentConfirm/(?P<Activation_key>\w+)', 'ParentConfirm', name = 'ParentConfirm'),
    url(r'^parentReview/$', 'parentReview', name = 'parentReview'),
    url(r'^ParentConfirmYes/$', 'ParentConfirmYes', name = 'ParentConfirmYes'),

)
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registrationApp/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'registrationApp/logout.html'}),    
)