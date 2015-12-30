from django.conf.urls import include, url
from django.contrib import admin
from scad.views import index
from scad.views import group_page
from scad.views import user_page
from scad.views import group_member_inf
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', index),
    url(r'^group/(?P<group_id>[0-9]+)/$',group_page),
    url(r'^user/(?P<user_id>[0-9]+)/$',user_page),
    url(r'^group/(?P<group_id>[0-9]+)/member_inf/$',group_member_inf),
]


