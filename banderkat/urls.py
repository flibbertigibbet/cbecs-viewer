from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from elec.views import hello,dbdemo,formdemo

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'banderkat.views.home', name='home'),
    # url(r'^banderkat/', include('banderkat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$',hello),
    url(r'^dbdemo/$',dbdemo),
	url(r'^formdemo/$',formdemo),

)
