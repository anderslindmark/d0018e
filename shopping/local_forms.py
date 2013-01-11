from django import forms

class CreateUser(forms.Form):
	"""
	This form decides what information is shown when creating a new user
	"""
	username = forms.CharField(max_length=30)
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField()
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)
	address = forms.CharField(max_length=150, widget=forms.Textarea)
	phone_number = forms.CharField(max_length=20, required=True) # required=False when model is updated

class CreateCustomer(forms.Form):
	"""
	This form decides what fields the user needs to enter when the customer-objects needs to be created for an existing user
	"""
	address = forms.CharField(max_length=150, widget=forms.Textarea, required=True)
	phone_number = forms.CharField(max_length=20, required=True) # required=False when model is updated

class PlaceOrder(forms.Form):
	"""
	Order confirmation form
	"""
	confirm = forms.BooleanField(label='Yes please!')

class EditAccount(forms.Form):
	"""
	This form is used when editing the account
	"""
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField()
	#password = forms.CharField(max_length=50, widget=forms.PasswordInput)
	address = forms.CharField(max_length=150, widget=forms.Textarea)
	phone_number = forms.CharField(max_length=20, required=True)
