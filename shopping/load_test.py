"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# https://docs.djangoproject.com/en/dev/topics/testing/
# http://stackoverflow.com/questions/465065/writing-unit-tests-in-django-python
# http://harry.pythonanywhere.com/

from django.test import TestCase
from django.test.client import Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class HomeTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_home(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

# TODO
# * Test login/logout
#	* Test access granted/denied for specific operations
# * Test each /url for 200
# * Test adding items to basket
# * Test removing items from basket
# * Test placing an order
#	* With no items

# * Test adding a new user (assert success)
# * Test adding a user with same username as an existing user (assert failure)
