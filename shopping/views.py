from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, render, redirect
from shopping.models import Category, Asset, Customer
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
	return render_to_response("account.html",
			{
				'logged_in': request.user.is_authenticated(),
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
