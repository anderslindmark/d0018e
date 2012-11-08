from django.conf.urls import patterns, include, url
import shopping

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'd0018e_project.views.home', name='home'),
    # url(r'^d0018e_project/', include('d0018e_project.foo.urls')),

	url(r'^$', 'shopping.views.index'),
	url(r'^shh', 'shopping.views.loggedinonly'),
	#url(r'/login', 'shopping.views.login'),
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^logout', 'django.contrib.auth.views.logout', 
		{'template_name': 'registration/logout.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
