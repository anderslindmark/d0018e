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
	#detailed_description = models.CharField(max_length=5000) # TODO: Add this

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
	image = models.ImageField(null=True, blank=True, upload_to='asset_images')

	def __unicode__(self):
		return self.name

	def __repr__(self):
		return "<Asset: name=%r, description=%r, category=%r, price=%r, stock=%r>" % (self.name, self.description, self.category, self.price, self.stock)

class Basket(models.Model):
	"""
	Shopping basket, contains a list of assets and which customer it belongs to.
	"""
	customer = models.ForeignKey(Customer)
	active = models.BooleanField(default=True) # Active = current basket, inactive = order
	# These two fields are only interesting when the basket becomes an order:
	date_placed = models.DateTimeField(null=True, blank=True) # Date the order was placed
	date_filled = models.DateTimeField(null=True, blank=True) # Date the order was filled 

	def __unicode__(self):
		status = "(current)" if self.active else "(order)"
		return str(self.customer) + "s shopping basket " + status

class BasketItem(models.Model):
	"""
	Maps assets to the basket
	"""
	basket = models.ForeignKey(Basket)
	asset = models.ForeignKey(Asset)
	count = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.basket) + ": " + str(self.count) + " * " + str(self.asset)
