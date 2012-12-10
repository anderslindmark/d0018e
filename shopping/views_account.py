from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from shopping.views_helpers import get_basket_total
from shopping.views_helpers import customer_required
from django.template import RequestContext
from django.shortcuts import render, redirect


@login_required
@customer_required
def show_account(request):
	"""
	Show a page with account information and order history.
	"""
	cust = Customer.objects.get(user=request.user)

	baskets = Basket.objects.filter(customer=cust).filter(active=False)
	orders = []
	for order in baskets:
		items = BasketItem.objects.filter(basket=order)
		orderinfo = dict()
		orderinfo['items'] = items
		orderinfo['basket'] = order
		orderinfo['total'] = get_basket_total(items) # This is not a good solution, since cost could have changed since order was placed
		orders.append(orderinfo)

	request_context = RequestContext(request, {
				'cust': cust,
				'orders': orders,
		})

	return render(request, "account.html", request_context)


def create_account(request):
	"""
	Create an account
	"""
	problems = []
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
				# The username already exists
				problems.append("Username already taken")
			else:	
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
				'problems': problems,
				})

	return render(request, "create_account.html", request_context)


@login_required
def create_missing_customer(request):
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

