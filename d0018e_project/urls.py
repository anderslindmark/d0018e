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

	url(r'^basket$', 'shopping.views.basket'),
	url(r'^basket/remove/(?P<itemID>\d+)$', 'shopping.views.remove_product'),
	url(r'^basket/remove/all$', 'shopping.views.remove_product'),
	url(r'^basket/update/(?P<itemID>\d+)/(?P<count>\d+)$', 'shopping.views.update_product_count'),

	url(r'^ajax/basket$', 'shopping.views.ajax_basket'),
	url(r'^ajax/addproduct/(?P<productID>\d+)$', 'shopping.views.ajax_addproduct'),





    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
