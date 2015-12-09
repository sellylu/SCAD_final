from django.conf.urls import include, url
from django.contrib import admin
from scad.views import index
from scad.views import show_inf
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^index/$', index),
	url(r'^show_inf/$',show_inf),
]

