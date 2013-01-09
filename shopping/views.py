from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem, Grade, GradeHistory, Comment
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from shopping.views_helpers import get_categories, get_or_create_basket, get_basket_total, add_rating, get_rating, fetch_comments
from shopping.views_helpers import customer_required
from shopping.views_helpers import comments_build_children_tree, comments_render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


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
	# Get asset
	asset = Asset.objects.get(pk=productID)

	# Get grade.
	rating = get_rating(productID)

	request_context = RequestContext(request, {
				'categories': get_categories(request),
				'asset': asset,
				'rating': rating,
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


@login_required
@customer_required
def asset_addgrade(request, productID, grade):
	"""
	Ajax-call to add a rating to a product
	"""
	try:
		# Sanity check input
		asset = Asset.objects.get(pk = productID) # Will throw an exception if no such object exists
		grade = int(grade)
		assert(grade >= 1 and grade <= 5)
	except:
		# Either the product does not exist or the grade was not between 1 and 5
		return HttpResponse("Denied")

	# Try to add rating
	cust = Customer.objects.get(user=request.user)
	if (add_rating(cust, productID, grade)):
		# Rating was added successfully
		return HttpResponse("Success")
	else:
		# Rating was denied, user has rated the product before
		return HttpResponse("Denied")
	

def get_comments(request, productID):
	"""
	Retrieve a list of comments for a specific product
	"""
	all_comments = fetch_comments(productID)
	if not all_comments:
		# No comments
		request_context = RequestContext(request, {
					'comments': None,
			})
	else:
		# There are comments
		base_comments = all_comments.filter(parent = None) # These are the base-comments (not a child to other comments)
		comment_list = []
		# Build the comment-tree
		for base_comment in base_comments:
			children = comments_build_children_tree(all_comments, base_comment)
			comment_list.append((base_comment, children))

		# Render the comment tree into html
		html = comments_render(0, comment_list)

		request_context = RequestContext(request, {
					'comments': html,
			})

	return render(request, "comments.html", request_context)

@login_required
@csrf_exempt
def add_comment(request, productID, replyTo=None):
	"""
	Add a comment to a product. Comment content is expected to be in POST data
	"""
	if not request.method == 'POST':
		return HttpResponse("Erroneous call")
	else:
		comment = request.POST['comment']
		if len(comment) < 10:
			return HttpResponse("Comment needs to been 10 characters or longer")
		try:
			asset = Asset.objects.get(pk = productID)
			customer = Customer.objects.get(user=request.user)
		except Asset.DoesNotExist:
			return HttpResponse("No such product")
		except Customer.DoesNotExist:
			return HttpResponse("Please fill in your account information")
		comment = Comment(asset=asset, customer=customer, comment=comment)
		comment.save()
		return HttpResponse("OK")
		
