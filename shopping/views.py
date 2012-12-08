from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from django.template import RequestContext
from django.contrib.auth.models import User

from datetime import datetime

# TODO: Write a @basket_required-decorator, 
#   alternatively a @customer_and_basket_required which redirects to /account_missing_info and later creates baskets (overkill?)
# TODO: Move code out to views_basket.py, views_account.py, etc

def _getCategories(request, current=None):
	"""
	Helper to setup the category list and make sure that the currently selected category persists 
	through the browsing session.
	"""
	# TODO: This does not use current yet
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
	asset = Asset.objects.get(pk=productID)

	request_context = RequestContext(request, {
				'categories': _getCategories(request),
				'asset': asset,
		})

	return render(request, "product.html", request_context)

@login_required
def account(request):
	"""
	Show a page with account information and order history.
	"""
	try:
		cust = Customer.objects.get(user=request.user)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')

	baskets = Basket.objects.filter(customer=cust).filter(active=False)
	orders = []
	for order in baskets:
		items = BasketItem.objects.filter(basket=order)
		orderinfo = dict()
		orderinfo['items'] = items
		orderinfo['basket'] = order
		orderinfo['total'] = _get_basket_total(items) # This is not a good solution, since cost could have changed since order was placed
		orders.append(orderinfo)

	request_context = RequestContext(request, {
				'cust': cust,
				'orders': orders,
		})

	return render(request, "account.html", request_context)

def create_customer_special(request):
	"""
	This is called if the current user does not have a Customer-object associated to it
	"""
	if request.method == 'POST':
		form = CreateCustomer(request.POST)
		if form.is_valid():
			address = form.cleaned_data['address']
			phone_number = form.cleaned_data['phone_number']
			user = request.user
			cust = Customer(address=address, phone_number=phone_number, user=user)
			cust.save()
			return redirect('/account/thankyou')
	else:
		form = CreateCustomer()
	request_context = RequestContext(request, {'form': form})
	return render(request, "create_customer.html", request_context)

@login_required
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

def thankyou(request):
	"""
	Shows a thank you message to the user
	"""
	request_context = RequestContext(request)
	return render(request, "thankyou.html", request_context)

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

def _get_basket_total(basket_items):
	"""
	Calculate total price for all items in the basket
	"""
	# Sum up prices and counts for all the assets in the basket
	#total = sum( [item.price*count for item,count in assets.iteritems()] )
	total = 0
	for item in basket_items:
		total += item.asset.price * item.count
	return total

@login_required
def basket(request):
	"""
	Show a page with shopping basket information
	"""
	try:
		basket = _get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
	items = BasketItem.objects.filter(basket=basket)
	total = _get_basket_total(items)

	request_context = RequestContext(request, {
		'items': items,
		'total': total,
	})

	return render(request, "basket.html", request_context)

@login_required
def place_order(request):
	try:
		basket = _get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
	items = BasketItem.objects.filter(basket=basket)
	total = _get_basket_total(items)

	problems = dict()

	if request.method == 'POST':
		form = PlaceOrder(request.POST)
		if form.is_valid():
			# User agreed to place the order, now check stock
			for item in items:
				if item.count > item.asset.stock:
					problems[item.asset.name] = "Only %d items in stock, you have ordered %d" % (item.asset.stock, item.count)

			if len(problems) == 0: # No problems, order can be placed
				# Decrease stock count, mark order as placed, a new shopping basket will automatically be created
				# Then redirect to /order/placed
				for item in items:
					item.asset.stock -= item.count # TODO: Is a save() needed?
					item.asset.save()

				basket.active = False
				basket.date_placed = datetime.now()
				basket.save()

				return redirect('/order/placed')

	else:
		form = PlaceOrder()
	
	request_context = RequestContext(request, {
		'items': items,
		'total': total,
		'form': form,
		'problems': problems,
	})
	
	return render(request, "place_order.html", request_context)

@login_required
def order_placed(request):
	request_context = RequestContext(request)
	return render(request, "order_placed.html", request_context)

@login_required
def ajax_basket(request):
	"""
	Show a mini-page with shopping basket, used for AJAX-tooltips.
	"""
	try:
		basket = _get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')

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
	try:
		basket = _get_or_create_basket(request)
		# Get the asset
		asset = Asset.objects.get(pk=productID)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
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
	try:
		basket = _get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
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
	try:
		basket = _get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')

	count = int(count)
	item = BasketItem.objects.filter(basket=basket).get(asset__pk = itemID)
	if count <= 0:
		item.delete()
	else:
		item.count = count
		item.save()
	
	return redirect('/basket')

