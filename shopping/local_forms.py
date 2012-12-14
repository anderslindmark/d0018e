from django import forms

class CreateUser(forms.Form):
	username = forms.CharField(max_length=30)
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField()
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)
	address = forms.CharField(max_length=150, widget=forms.Textarea)
	phone_number = forms.CharField(max_length=20, required=True) # required=False when model is updated

class CreateCustomer(forms.Form):
	address = forms.CharField(max_length=150, widget=forms.Textarea, required=True)
	phone_number = forms.CharField(max_length=20, required=True) # required=False when model is updated

class PlaceOrder(forms.Form):
	confirm = forms.BooleanField(label='Yes please!')

class EditAccount(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField()
	#password = forms.CharField(max_length=50, widget=forms.PasswordInput)
	address = forms.CharField(max_length=150, widget=forms.Textarea)
	phone_number = forms.CharField(max_length=20, required=True)
