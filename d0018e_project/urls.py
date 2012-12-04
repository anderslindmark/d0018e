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

	url(r'^category/(?P<category>.+)$', 'shopping.views.showcategory'),
	url(r'^product/(?P<productID>\d+)$', 'shopping.views.showproduct'),

	url(r'^account/me$', 'shopping.views.account'),
	url(r'^account/create$', 'shopping.views.create_account'),
	url(r'^account/welcome$', 'shopping.views.welcome'),
	url(r'^account/login', 'django.contrib.auth.views.login',
		{'template_name': 'login.html'}),
	url(r'^account/logout', 'django.contrib.auth.views.logout', 
		{'template_name': 'logout.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
