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

class Category(models.Model):
	"""
	Represents a group of specific assets, i.e if we are selling food then "Snacks" could be a category
	"""
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)

class Asset(models.Model):
	"""
	Represents a product.
	"""
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	category = models.ForeignKey(Category) # Which category does this asset belong to
	stock = models.IntegerField() # How many of this asset are in stock

class Basket(models.Model):
	"""
	Shopping basket, contains a list of assets and which customer it belongs to.
	"""
	assets = models.ManyToManyField(Asset)
	customer = models.ForeignKey(Customer)

class Order(models.Model):
	"""
	A placed order, contains information about which assets was ordered, which customer placed the order and
	when the order was placed/shipped.
	"""
	assets = models.ManyToManyField(Asset)
	customer = models.ForeignKey(Customer)
	date_placed = models.DateTimeField(auto_now=True) # Date the order was placed
	date_filled = models.DateTimeField() # Date the order was filled 


