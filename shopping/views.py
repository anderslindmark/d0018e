from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from shopping.models import Category, Asset

# Create your views here.

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
	return render_to_response("home.html", {'categories': _getCategories(request)})

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
			})

def showproduct(request, productID):
	print "product id:", str(productID)
	return render_to_response("product.html", {'categories': _getCategories(request)})

def account(request):
	return render_to_response("account.html")

@login_required
def loggedinonly(request):
	return HttpResponse("Shh")

