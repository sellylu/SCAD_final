from django.conf.urls import include, url
from django.contrib import admin
from scad.views import index
from scad.views import group_page
from scad.views import user_page
from scad.views import group_member_inf
from scad.views import userno
from scad.views import getcalendarevent
from scad.views import postcalendarevent
from scad.views import deletecalendarevent

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^index/$', index),
    url(r'^group/(?P<group_id>[0-9]+)/$',group_page),
    url(r'^user/(?P<user_id>[0-9]+)/$',user_page),
    url(r'^group/(?P<group_id>[0-9]+)/member_inf/$',group_member_inf),
    url(r'^userno/(?P<user_id>[0-9]+)/$',userno),
    url(r'^group/(?P<group_id>[0-9]+)/calendar/$',getcalendarevent),
    url(r'^postcalendarevent/(?P<group_id>[0-9]+)/$',postcalendarevent),
    url(r'^deletecalendarevent/(?P<group_id>[0-9]+)/$',deletecalendarevent),
]