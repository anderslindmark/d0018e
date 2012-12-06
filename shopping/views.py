from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser
from django.template import RequestContext
from django.contrib.auth.models import User

# TODO: Find out how to send the same context chunk to _all_ render*()-calls

def _getCategories(request, current=None):
	"""
	Helper to setup the category list and make sure that the currently selected category persists through the session.
	"""
	# Get Categories
	# Mark current cat somehow (maybe just add a field cat.isSelected = False except for if cat == current_category)
	# https://docs.djangoproject.com/en/1.4/topics/templates/
	current_category = request.session.get('current_category')
	categories = Category.objects.all()
	if current is not None:
		for cat in categories:
			if cat.name == current:
				print "Setting current to:", str(cat.name)
				cat.current = True
	return categories

def index(request):
	#return HttpResponse("Hej")
	if request.user.is_authenticated():
		print "User is authed"
	else:
		print "User is NOT authed"
	return render_to_response("home.html", 
			{
				'categories': _getCategories(request),
				'logged_in': request.user.is_authenticated(),
			})

def showcategory(request, category):
	print "category:", str(category)
	# Get all items related to that category
	cat = Category.objects.get(name=category)
	products = Asset.objects.filter(category=cat)
	return render_to_response("category.html", 
			{
				'categories': _getCategories(request, current=category),
				'category': cat,
				'products': products,
				'logged_in': request.user.is_authenticated(),
			})

def showproduct(request, productID):
	print "product id:", str(productID)
	return render_to_response("product.html", 
			{
				'categories': _getCategories(request),
				'logged_in': request.user.is_authenticated(),
			})

@login_required
def account(request):
	print type(request.user)
	cust = Customer.objects.get(user=request.user)

	return render_to_response("account.html",
			{
				'logged_in': request.user.is_authenticated(),
				'user': request.user,
				'cust': cust,
			})

def create_account(request):
	if request.method == 'POST':
		# Form is submitted
		form = CreateUser(request.POST)
		if form.is_valid():
			print "Form is valid"
			# Get form-data
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			phone_number = form.cleaned_data['phone_number']

			# Do extra validation:
			# Check if username is available:
			users = User.objects.filter(username=username)
			if not len(users) == 0:
				pass
				# FAIL: The username is already taken
				# TODO: Return the error and show the form-page again
			
			# We could do more checks here, for instance unique e-mail. But we won't...
			# Create the User object:
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			
			# Create the Customer object:
			cust = Customer(address=address, phone_number=phone_number, user=user)
			cust.save()

			# The user-account is now created. Log in and redirect to welcome.html
			u_auth = authenticate(username=username, password=password)
			# Make sure that authentication was successful.
			# Iwe can't authenticate the newly created user, something is very wrong..
			assert type(u_auth) is not None 
			login(request, u_auth)

			# Send user to the welcome page:
			return redirect('/account/welcome')	
	else:
		form = CreateUser()

	# Either form will be a newly created one, or an old one with information attached
	reqcon = RequestContext(request, {
				'logged_in': request.user.is_authenticated(),
				'form': form,
				})

	return render(request, "create_account.html", reqcon)

@login_required
def welcome(request):
	return render_to_response("welcome.html", {
				'logged_in': request.user.is_authenticated(),
				'name': request.user.first_name,
				})

def get_or_create_basket(request):
	# Helper method
	cust = Customer.objects.get(user=request.user)
	try:
		basket = Basket.objects.exclude(active=False).get(customer=cust)
		print "Using existing basket"
	except Basket.DoesNotExist:
		print "Creating new basket"
		basket = Basket(customer=cust)
		basket.save()
	return basket

def build_asset_table(basket):
	# Build count-table (dict of asset -> count)
	asset_dict = dict()
	# Get all assets
	basket_items = BasketItem.objects.filter(basket=basket)
	for basket_item in basket_items:
		asset = basket_item.asset
		if asset_dict.has_key(asset):
			asset_dict[asset] += 1
		else:
			asset_dict[asset] = 1
	return asset_dict

@login_required
def basket(request):
	basket = get_or_create_basket(request)
	assets = build_asset_table(basket)
	total = sum( [item.price*count for item,count in assets.iteritems()] )

	return render_to_response("basket.html", {
		'logged_in': request.user.is_authenticated(),
		'assets': assets.iteritems, # iteration of i,j will give asset,count pairs
		'total': total,
		})

@login_required
def ajax_basket(request):
	basket = get_or_create_basket(request)
	assets = build_asset_table(basket)

	return render_to_response("ajax_basket.html", {
		'assets': assets.iteritems,
		})

@login_required
def ajax_addproduct(request, productID):
	basket = get_or_create_basket(request)
	try:
		asset = Asset.objects.get(pk=productID)
	except Asset.DoesNotExist:
		print "Product not found!"
		return HttpResponse("Error: No such product")
	basket_item = BasketItem(basket=basket, asset=asset)
	basket_item.save()
	return HttpResponse("OK")

@login_required
def remove_product(request, itemID=-1):
	basket = get_or_create_basket(request)
	if itemID == -1:
		# If itemID == -1 then all items will be removed.
		BasketItem.objects.filter(basket=basket).delete()
	else:
		# TODO: This doesn't bulk-delete a number of assets. A set_item_count(asset) method is needed. Or just a count= parameter to this method.
		try:
			# BasketItem.objects.get(pk=itemID).delete()
			items = BasketItem.objects.filter(basket=basket).filter(asset__pk = itemID)
			for item in items:
				item.delete()
		except BasketItem.DoesNotExist:
			pass

	return redirect('/basket')

@login_required
def update_product_count(request, itemID, count):
	# This isn't a very pretty way of doing things... but it'll have to do for now.
	basket = get_or_create_basket(request)
	count = int(count)
	# First get all items of this type from the basket
	try:
		current_items = BasketItem.objects.filter(basket=basket).filter(asset__pk = itemID)
	except BasketItem.DoesNotExist:
		print "Error: No basket items found" # This only happens if rows are deleted after rendering /basket (i.e two open tabs or old session)
		return redirect('/basket')
	asset = current_items[0].asset
	diff = abs(len(current_items) - count)
	# Check if we need to add or delete items to reach 'count'
	if len(current_items) < count:
		# Add item(s)
		for i in xrange(diff):
			b = BasketItem(basket=basket, asset=asset)
			b.save()
	elif len(current_items) > count:
		# Remove item(s)
		iter = current_items.iterator()
		for i in xrange(diff):
			item = iter.next()
			item.delete()
	
	return redirect('/basket')





