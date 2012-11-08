from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
	return HttpResponse("Hej")

@login_required
def loggedinonly(request):
	return HttpResponse("Shh")

