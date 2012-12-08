from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from shopping.models import Category, Asset, Customer, Basket, BasketItem
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from shopping.views_helpers import get_or_create_basket, get_basket_total
from django.template import RequestContext
from django.shortcuts import render, redirect

from datetime import datetime


@login_required
def basket(request):
	"""
	Show a page with shopping basket information
	"""
	try:
		basket = get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
	items = BasketItem.objects.filter(basket=basket)
	total = get_basket_total(items)

	request_context = RequestContext(request, {
		'items': items,
		'total': total,
	})

	return render(request, "basket.html", request_context)


@login_required
def remove_product(request, itemID=-1):
	"""
	Remove all occurences of a product (or all products, if itemID = -1) from the shopping basket. 
	Redirects back to /basket since that is the only place it will be called from.
	"""
	try:
		basket = get_or_create_basket(request)
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
		basket = get_or_create_basket(request)
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


@login_required
def place_order(request):
	try:
		basket = get_or_create_basket(request)
	except Customer.DoesNotExist:
		return redirect('/account/missing_info')
	items = BasketItem.objects.filter(basket=basket)
	total = get_basket_total(items)

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
		basket = get_or_create_basket(request)
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
		basket = get_or_create_basket(request)
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

