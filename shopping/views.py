from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from shopping.models import Category, Asset, Customer, Basket, BasketItem, Grade, GradeHistory, Comment
from shopping.local_forms import CreateUser, CreateCustomer, PlaceOrder
from shopping.views_helpers import get_categories, get_or_create_basket, get_basket_total, add_rating, get_rating, fetch_comments
from shopping.views_helpers import customer_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

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

	# Get grade.
	# TODO: Add this in the report:
	#	There are a few ways to do grading.
	#	- 1 -
	#	One could add a table with a foreign key to the asset, a foregin key to the customer
	#	and the grade.
	#	The advantage of this system is that every review is trackable, and the user can even go in and
	#	change the grade.
	#	The disadvantage is that if there are n customers and m products, and all customers grade every
	#	product there will be n*m rows in this table.
	#	Every time a product-page is fetched and the review is calculated we would have to fetch n rows from
	#	the table to calculate the grade.
	#	- 2 -
	#	The second way is to simply keep a table with a foreign key to the asset, an int-field `count'
	#	and an int-field `sum'. Every time a product is rated the count-field will be increased by 1 and
	#	the grade will be added to the sum. Calculating the grade consists of fetching the one row from the
	#	database and evaluating sum/count.
	#	This has the advantage of being fast and easy.
	#	The disadvantage is that a customer can keep rating the same product over and over again and thus
	#	skewing the total grade of the product.
	#	- 3 -
	#	The third option is a compromise between the two previous methods.
	#	In the same way as method 2 a grade-table is kept that consists of asset(FK), count(int) and sum(int).
	#	There is however a second table, GradeHistory, that has two fields: 
	#		customer(FK) and history(varchar/text).
	#	The history-field consists of a comma-separated list of which product-id's that user has rated.
	#	When a customer tries to rate a product that customers GradeHistory-row is fetched and a check is done
	#	to see if product-id is in the history-list. If it is not, the grade is accepted and the product-id
	#	is added to the history.
	#	The same problem exists here, what if all n customers rate all m products? Then the history field
	#	would become very big. It will still only be one row that is fetched, though.
	#	Limiting the size of the history-field is easy, one can simple settle with keeping a history of the
	#	last k grades, and if adding the grade to history causes it to be of length k+1 then pop()ing the
	#	fist grade will keep it in check. This way a user can still vote more times for the same product, but
	#	only after having first voted for a number of other products. I have chosen to limit the history to
	#	200 items, since they are stored as a comma-separated list ("1,2,3,4") storing 200 items requires
	#	a length of 200*2-1 = 399 ~= 400. However these product-ids can be longer than 1 digit so I set the
	#	length to 1000 and we will have to accept that the number of votes is a bit arbitrary.
	#	This way grades are fast to fetch and set (2 reads, 2 writes, at most) and the database wont grow
	#	out of control with a large number of users and products.

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
	# Sanity check input
	try:
		productID = int(productID) # TODO: check if a product with this id exists?
		grade = int(grade)
		assert(grade <= 5)
		assert(grade >= 1)
	except:
		return HttpResponse("Denied")

	# Get rating-history
	cust = Customer.objects.get(user=request.user)
	if (add_rating(cust, productID, grade)):
		# Rating was added successfully
		return HttpResponse("Success")
	else:
		return HttpResponse("Denied")
	
def asset_getgrade(request, productID):
	"""
	Retrieve the rating for a product. Returns "No ratings" if no ratings are available
	"""
	# TODO: will this view be used?

	rating = get_rating(productID)
	if rating:
		grade, count = rating
		return HttpResponse(str(grade))
	else:
		return HttpResponse("No ratings")

def get_comments(request, productID):
	"""
	Retrieve a list of comments for a specific product
	"""
	comments = fetch_comments(productID)
	request_context = RequestContext(request, {
				'comments': comments,
		})
	return render(request, "comments.html", request_context)

@login_required
@csrf_exempt
def add_comment(request, productID):
	"""
	Add a comment to a product. Comment content is expected to be in POST data
	"""
	if not request.method == 'POST':
		return HttpResponse("NOOOOOO!")
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
		


