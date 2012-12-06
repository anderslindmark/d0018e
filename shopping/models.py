from django.db import models
from django.contrib.auth.models import User

# A list of field types, and options related to the field types:
#  https://docs.djangoproject.com/en/dev/ref/models/fields/#
# Django comes with a user-system, so some fields are already available for an authenticated user:
#  https://docs.djangoproject.com/en/dev/topics/auth/ 

class Customer(models.Model):
	"""
	Contains extra information about a customer other than the fields that are available in django-auth.
	"""
	# For now, store all address info in one field, i.e "Bob Bobster\n13Bob street\nBobtown"
	address = models.CharField(max_length=150) 
	phone_number = models.CharField(max_length=20)
	user = models.OneToOneField(User) # The user-field points into django's own auth-system.

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name

class Category(models.Model):
	"""
	Represents a group of specific assets, i.e if we are selling food then "Snacks" could be a category
	"""
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)

	def __unicode__(self):
		return self.name

	def __repr__(self):
		return "<Category: name=%r, description=%r>" % (self.name, self.description)

class Asset(models.Model):
	"""
	Represents a product.
	"""
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	category = models.ForeignKey(Category) # Which category does this asset belong to
	price = models.IntegerField()
	stock = models.IntegerField() # How many of this asset are in stock

	def __unicode__(self):
		return self.name

	def __repr__(self):
		return "<Asset: name=%r, description=%r, category=%r, price=%r, stock=%r>" % (self.name, self.description, self.category, self.price, self.stock)

class Basket(models.Model):
	"""
	Shopping basket, contains a list of assets and which customer it belongs to.
	"""
	customer = models.ForeignKey(Customer)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.customer) + "s shopping basket"

class BasketItem(models.Model):
	"""
	Maps assets to the basket
	"""
	basket = models.ForeignKey(Basket)
	asset = models.ForeignKey(Asset)

class Order(models.Model):
	"""
	A placed order, contains information about which assets was ordered, which customer placed the order and
	when the order was placed/shipped.
	"""
	basket = models.ForeignKey(Basket)
	# TODO: move these two fields into basket. if basket.active = False then it is an order and these two fields are used
	date_placed = models.DateTimeField(auto_now=True) # Date the order was placed
	date_filled = models.DateTimeField() # Date the order was filled 


