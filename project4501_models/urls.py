from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/users/$',views.user_list),
    url(r'^api/v1/users/(?P<pk>[0-9]+)$', views.user_detail),

    url(r'^api/v1/courses/$',views.course_list),
    url(r'^api/v1/courses/(?P<pk>[0-9]+)$',views.course_detail),


    url(r'^api/v1/courses/(?P<pk>[0-9]+)/sessions/$',views.session_list),
    url(r'^api/v1/courses/(?P<pk1>[0-9]+)/sessions/(?P<pk2>[0-9]+)$',views.session_detail),
)