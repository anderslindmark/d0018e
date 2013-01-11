from shopping.models import Category, Asset, Customer, Basket, BasketItem, Grade, GradeHistory, Comment
from django.shortcuts import redirect
from django.template.loader import render_to_string

def get_categories(request, current=None):
	"""
	Helper to setup the category list and make sure that the currently selected category persists 
	through the browsing session.
	"""
	# Get Categories
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


def customer_required(func, redirect_url='/account/missing_info'):
	"""
	Decorator that removes the need for manual missing-customer checks
	everywhere
	"""
	# This inner function runs the decorated function with some checks
	def check(request, *args, **kwargs):
		try:
			return func(request, *args, **kwargs)
		except Customer.DoesNotExist:
			return redirect(redirect_url)
	
	# Return the modified function 
	return check

def add_rating(customer, productID, rating):
	"""
	Add a rating to a product. Returns False if the rating was not allowed, True otherwise
	"""
	try:
		gradehist = GradeHistory.objects.get(customer=customer)
	except GradeHistory.DoesNotExist:
		# First time the customer rates something, create GradeHistory
		gradehist = GradeHistory(customer=customer)
		gradehist.save()
	
	history_list = gradehist.history.split(',') # ['1', '2', '9']
	if str(productID) in history_list:
		# User has already rated this product
		return False
	else:
		# User has not already rated this product. At least not recently
		# Try to get existing ratings
		try:
			grade = Grade.objects.get(asset__pk = productID)
		except Grade.DoesNotExist:
			try:
				asset = Asset.objects.get(pk = productID)
			except Asset.DoesNotExist:
				return False
			grade = Grade(asset = asset)
		grade.count += 1
		grade.sum += rating
		grade.save()
		# Add this to the rating history
		print repr(history_list)
		if gradehist.history == "":
			gradehist.history = str(productID)
		else:
			history_list.append(str(productID))
			print repr(history_list)
			history = ','.join(history_list)
			while len(history) > 1000:
				# History is too long, cut of first element until length is good
				history = history[ history.find(',')+1 : ]
			gradehist.history = history
		gradehist.save()
		return True

def get_rating(productID):
	"""
	Retrieve the rating for a product. Returns False if no ratings are available
	"""
	try:
		grade_obj = Grade.objects.get(asset__pk = productID)
	except Grade.DoesNotExist:
		try:
			asset = Asset.objects.get(pk = productID)
		except Asset.DoesNotExist:
			return False
		grade_obj = Grade(asset = asset)
	if grade_obj.count == 0:
		return False
	else:
		grade = grade_obj.sum/float(grade_obj.count)
		return (grade, grade_obj.count)

def fetch_comments(productID):
	"""
	Retrieve a list of comments for a product. Returns False if no comments are available
	"""
	try:
		comments = Comment.objects.filter(asset__pk = productID).order_by('-timestamp')
	except Comment.DoesNotExist:
		return False
	return comments

def comments_build_children_tree(all_comments, base_comment):
	"""
	Build a comment tree for one comment (base_comment). 
	Direct children will be all the comments in all_comment whose 'parent'-field points to base_comments, and so on.
	Will return a list of tuples. A comment with no children will consist of the tuple (comment, None),
	a comment with children will consist of the tuple (comment, [childlist]) where childlist is a list created recursively by this function.
	Example:
	[
		(comment_1, None),
		(comment_2, [
						(comment_4, [
										(comment_6, None)
									]),
						(comment_5, None)
					]),
		(comment_3, None)
	]
	"""
	child_list = []
	children = all_comments.filter(parent = base_comment)
	if len(children) == 0:
		return None

	for child in children:
		child_children = comments_build_children_tree(all_comments, child)
		child_list.append( (child, child_children) )
	
	return child_list

def comments_render(indent_level, commentlist):
	"""
	Renders a comment-tree (as produced by comments_build_children_tree()) using a template and returns the raw html.
	"""
	html = ""
	for comment, children in commentlist:
		# Render base comment
		padding = 15 + indent_level * 15
		html += render_to_string('single_comment.html', {'comment': comment, 'padding': padding })
		if children is not None:
			# Render child-comments if they exist
			html += comments_render(indent_level+1, children)
	return html
