#!/usr/bin/env python
#DJANGO_SETTINGS_MODULE=d0018e_project.settings python populatedb.py
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'd0018e_project.settings'

from shopping.models import Customer, Category, Asset, Basket

categories = [
		('socks', 'Items to put on your feet'),
		('shoes', 'Items to put on your socks'),
		('fruit', "Eat this, it's good for you"),
		('telephones', 'Put one end against your ear and shout in the other'),
		]

for n, d in categories:
	c = Category(name=n, description=d)
	c.save()

sockCat = Category.objects.get(name='socks')
shoeCat = Category.objects.get(name='shoes')
fruitCat = Category.objects.get(name='fruit')
telCat = Category.objects.get(name='telephones')
products = [
		# (name, description, category, price, stock)
		('blue sock', 'An exquisite blue sock, fit for kings and queens alike', sockCat, 10, 100),
		('green sock', 'A sock of the green persuasion', sockCat, 10, 100),
		('gray sock', 'This sock lacks color', sockCat, 10, 75),

		('boot', 'A boot (or two boots to be specific)', shoeCat, 25, 100),
		('loafer', 'A loafer, slip it on and forget all about it', shoeCat, 20, 100),
		
		('banana', 'A yellow fruit, not very round at all', fruitCat, 8, 200),
		('pear', 'This fruit is a bit more round than the banana', fruitCat, 7, 150),
		('apple', "Currently this is the roundest fruit we've got!", fruitCat, 6, 200),

		('fixed phone', "This is where it's at", telCat, 100, 50),
		('mobile phone', "Everywhere is where it's at", telCat, 200, 300)
		]

for n, d, c, p, s in products:
	a = Asset(name=n, description=d, category=c, price=p, stock=s)
	a.save()


