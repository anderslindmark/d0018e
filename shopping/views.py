from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from shopping.views_helpers import get_categories, get_or_create_basket, get_basket_total
from django.template import RequestContext
from django.contrib.auth.models import User

# TODO: Write a @basket_required-decorator, 
#   alternatively a @customer_and_basket_required which redirects to /account_missing_info and later creates baskets (overkill?)


def index(request):
	"""
	Shows the home page
	"""
	request_context = RequestContext(request, {
				'categories': get_categories(request),
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
				'categories': get_categories(request, current=category),
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
				'categories': get_categories(request),
				'asset': asset,
		})

	return render(request, "product.html", request_context)


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

