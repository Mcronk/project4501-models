from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/authenticator/check/$',views.check_authenticator),
	url(r'^api/v1/authenticator/login/$',views.login),
	#need to change to specific authenticator
    url(r'^api/v1/authenticator/logout/$',views.logout),

    url(r'^api/v1/user/$',views.user_list),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', views.user_detail),

    url(r'^api/v1/course/$',views.course_list),
    url(r'^api/v1/course/(?P<pk>[0-9]+)$',views.course_detail),


    url(r'^api/v1/course/(?P<pk>[0-9]+)/session/$',views.session_list),
    url(r'^api/v1/course/(?P<pk1>[0-9]+)/session/(?P<pk2>[0-9]+)$',views.session_detail),
)