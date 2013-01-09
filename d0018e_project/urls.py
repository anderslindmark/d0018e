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

	# Account-related pages
	url(r'^account$', 'shopping.views_account.show_account'),
	url(r'^account/create$', 'shopping.views_account.create_account'),
	url(r'^account/missing_info', 'shopping.views_account.create_missing_customer'),
	url(r'^account/edit', 'shopping.views_account.edit_account'),
	url(r'^account/welcome$', 'shopping.views.welcome'),
	url(r'^account/thankyou$', 'shopping.views.thankyou'),
	url(r'^account/login', 'django.contrib.auth.views.login',
		{'template_name': 'login.html'}),
	url(r'^account/logout', 'django.contrib.auth.views.logout', 
		{'template_name': 'logout.html'}),

	# Basket and order related pages
	url(r'^basket$', 'shopping.views_basket.basket'),
	url(r'^basket/remove/(?P<itemID>\d+)$', 'shopping.views_basket.remove_product'),
	url(r'^basket/remove/all$', 'shopping.views_basket.remove_product'),
	url(r'^basket/update/(?P<itemID>\d+)/(?P<count>\d+)$', 'shopping.views_basket.update_product_count'),
	url(r'^order$', 'shopping.views_basket.place_order'),
	url(r'^order/placed$', 'shopping.views_basket.order_placed'),

	# AJAX-pages
	url(r'^ajax/basket$', 'shopping.views_basket.ajax_basket'),
	url(r'^ajax/addproduct/(?P<productID>\d+)$', 'shopping.views_basket.ajax_addproduct'),
	url(r'^ajax/addrating/(?P<productID>\d+)/(?P<grade>\d+)$', 'shopping.views.asset_addgrade'),
	#url(r'^ajax/getgrade/(?P<productID>\d+)$', 'shopping.views.asset_getgrade'),
	url(r'^ajax/comments/add/(?P<productID>\d+)$', 'shopping.views.add_comment'),
	url(r'^ajax/comments/add/(?P<productID>\d+)/(?P<replyTo>\d+)$', 'shopping.views.add_comment'),
	url(r'^ajax/comments/(?P<productID>\d+)$', 'shopping.views.get_comments'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
