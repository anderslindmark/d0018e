from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser
from django.template import RequestContext
from django.contrib.auth.models import User

def _getCategories(request, current=None):
	"""
	Helper to setup the category list and make sure that the currently selected category persists 
	through the browsing session.
	"""
	# Get Categories
	current_category = request.session.get('current_category') # ??
	categories = Category.objects.all()
	if current is not None:
		for cat in categories:
			if cat.name == current:
				cat.current = True # ??
	return categories

def index(request):
	"""
	Shows the home page
	"""
	request_context = RequestContext(request, {
				'categories': _getCategories(request),
		})
	return render(request, "home.html", request_context)

def showcategory(request, category):
	"""
	Shows a page with all products related to a category
	"""
	# Get the category object
	cat = Category.objects.get(name=category)
	# Get all products belonging to taht category
	products = Asset.objects.filter(category=cat)

	request_context = RequestContext(request, {
				'categories': _getCategories(request, current=category),
				'category': cat,
				'products': products,
		})

	return render(request, "category.html", request_context)

def showproduct(request, productID):
	"""
	Show a page with information about a specific product
	"""
	# TODO: Implement this
	request_context = RequestContext(request, {
				'categories': _getCategories(request),
		})

	return render(request, "product.html", request_context)

@login_required
def account(request):
	"""
	Show a page with account information and order history.
	"""
	cust = Customer.objects.get(user=request.user)

	# TODO: Fetch order history

	request_context = RequestContext(request, {
				'cust': cust,
		})

	return render(request, "account.html", request_context)

def create_account(request):
	"""
	Create an account
	"""
	# TODO: Move the 'create customer'-part (atleast) to a helper and then run that
	#		method (with a check) at login, so that all users are guaranteed to have
	#		a customer-object. (This is needed for the super-user created at ./manage.py syncdb)
	if request.method == 'POST':
		# Form is submitted
		form = CreateUser(request.POST)
		if form.is_valid():
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
			
			# We could do more checks here, for instance "is e-mail unique". But we won't...
			# Create the User object:
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			
			# Create the Customer object:
			cust = Customer(address=address, phone_number=phone_number, user=user)
			cust.save()

			# The user-account is now created. 
			# Log in and redirect to welcome.html:
			# Authenticate (this needs to be done before login())
			u_auth = authenticate(username=username, password=password)
			# Make sure that authentication was successful, if we can't authenticate the newly created 
			# user, something is very wrong..
			assert type(u_auth) is not None 

			# Log on the user:
			login(request, u_auth)

			# Send user to the welcome page:
			return redirect('/account/welcome')	
	else:
		# Start a new, blank, form
		form = CreateUser()

	# Either form will be a newly created one, or an old one with information attached
	request_context = RequestContext(request, {
				'form': form,
				})

	return render(request, "create_account.html", request_context)

@login_required
def welcome(request):
	"""
	Shows a welcome messge to a newly created user
	"""
	request_context = RequestContext(request)
	return render(request, "welcome.html", request_context)

def _get_or_create_basket(request):
	"""
	Helper method used to either fetch the users current shopping-basket,
	or create a new basket if no current basket exists.
	This way, the user always has a basket that is saved between sessions.
	"""
	# Fetch customer object
	cust = Customer.objects.get(user=request.user)
	try:
		# Get the current basket
		basket = Basket.objects.exclude(active=False).get(customer=cust)
	except Basket.DoesNotExist:
		# Create new basket
		basket = Basket(customer=cust)
		basket.save()
	return basket

@login_required
def basket(request):
	"""
	Show a page with shopping basket information
	"""
	basket = _get_or_create_basket(request)
	items = BasketItem.objects.filter(basket=basket)
	# Sum up prices and counts for all the assets in the basket
	#total = sum( [item.price*count for item,count in assets.iteritems()] )
	total = 0
	for item in items:
		total += item.asset.price * item.count

	request_context = RequestContext(request, {
		'items': items,
		'total': total,
		})

	return render(request, "basket.html", request_context)

@login_required
def ajax_basket(request):
	"""
	Show a mini-page with shopping basket, used for AJAX-tooltips.
	"""
	basket = _get_or_create_basket(request)
	items = BasketItem.objects.filter(basket=basket)

	request_context = RequestContext(request, {
			'items': items,
			})
	return render(request, "ajax_basket.html", request_context)

@login_required
def ajax_addproduct(request, productID):
	"""
	Called using an AJAX call when adding a product to the shopping basket
	"""
	basket = _get_or_create_basket(request)
	try:
		# Get the asset
		asset = Asset.objects.get(pk=productID)
	except Asset.DoesNotExist:
		print "Product not found!"
		return HttpResponse("Error: No such product")
	# Get or create a new BasketItem associated with the user and the product
	try:
		basket_item = BasketItem.objects.filter(basket=basket).get(asset__pk = productID)
	except:
		basket_item = BasketItem(basket=basket, asset=asset)
	basket_item.count += 1
	basket_item.save()
	return HttpResponse("OK")

@login_required
def remove_product(request, itemID=-1):
	"""
	Remove all occurences of a product (or all products, if itemID = -1) from the shopping basket. 
	Redirects back to /basket since that is the only place it will be called from.
	"""
	basket = _get_or_create_basket(request)
	if itemID == -1:
		# If itemID == -1 then all items will be removed.
		BasketItem.objects.filter(basket=basket).delete()
	else:
		try:
			# BasketItem.objects.get(pk=itemID).delete()
			item = BasketItem.objects.filter(basket=basket).get(asset__pk = itemID)
			item.delete()
		except BasketItem.DoesNotExist:
			# Since no BasketItem with this asset exists, our job is already done.
			pass

	return redirect('/basket')

@login_required
def update_product_count(request, itemID, count):
	"""
	Change the number of instances of a specific product that exists in our database.
	"""
	# TODO: Obviously BasketItem needs a 'count' parameter, this needs to be changed (ffs)
	basket = _get_or_create_basket(request)
	count = int(count)
	item = BasketItem.objects.filter(basket=basket).get(asset__pk = itemID)
	if count <= 0:
		item.delete()
	else:
		item.count = count
		item.save()
	
	return redirect('/basket')

