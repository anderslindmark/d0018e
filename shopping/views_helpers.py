from shopping.models import Category, Asset, Customer, Basket, BasketItem

def get_categories(request, current=None):
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

def get_or_create_basket(request):
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

def get_basket_total(basket_items):
	"""
	Calculate total price for all items in the basket
	"""
	# Sum up prices and counts for all the assets in the basket
	#total = sum( [item.price*count for item,count in assets.iteritems()] )
	total = 0
	for item in basket_items:
		total += item.asset.price * item.count
	return total

