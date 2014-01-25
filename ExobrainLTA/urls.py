from django.conf.urls import patterns, include, url
from django.contrib import admin
import ExobrainLTA.views

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
#    url(r'^$', 'project.views.home', name='home'),
#    url(r'^join/$', ExobrainLTA.views.show_join),
    url(r'^$', ExobrainLTA.views.show_login),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

#===============================================================================
# Task
#===============================================================================

    url(r'^api/task/$', ExobrainLTA.views.task_view),

    #url(r'^api/timeline/create/$', ExobrainLTA.views.message_create_view),

#===============================================================================
# SubTask
#===============================================================================
    url(r'^api/subtask/$', ExobrainLTA.views.subtask_view),
    
#===============================================================================
# Validation
#===============================================================================
    url(r'^api/validation/$', ExobrainLTA.views.validation_view),
    url(r'^api/validation/create/$', ExobrainLTA.views.validation_create_view),

#===============================================================================
# Timeline
#===============================================================================
    url(r'^api/timeline/$', ExobrainLTA.views.timeline_view),
    url(r'^api/timeline/create/$', ExobrainLTA.views.message_create_view),
    

#===============================================================================
# User
#===============================================================================

    url(r'^api/user/(?P<method>create)/$', ExobrainLTA.views.user_view),
    url(r'^api/user/(?P<method>update)/$', ExobrainLTA.views.user_view),
    url(r'^api/user/(?P<method>list)/$', ExobrainLTA.views.user_view),

    url(r'^api/login/$', ExobrainLTA.views.login_view),

    # Added to serve html

    url(r'^(?P<page>\w+).html$', ExobrainLTA.views.serve_html),
    
    
)
