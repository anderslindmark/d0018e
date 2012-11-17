from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

# Create your views here.

def index(request):
	#return HttpResponse("Hej")
	return render_to_response("home.html")

@login_required
def loggedinonly(request):
	return HttpResponse("Shh")

