from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('registrationApp.views',
    url(r'^registrationApp/$', 'index'),
    url(r'^registrationApp/(?P<student_id>\d+)/$', 'detail'),
    url(r'^registrationApp/(?P<student_id>\d+)/search/$', 'search'),
)
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)