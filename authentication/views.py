from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import base64
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def login(request):
	if request.method == "POST":
		email 			= request.POST.get("emailId")
		token 			= base64.b64encode(email.encode('utf-8')).decode('utf-8')
		html_message 	= f"""<p>Hi there,</p><p>Here is your <a href="https://magic-url-project.herokuapp.com/confirmation/{token}">magic link</a></p><p>Thanks,</p><p>Django Admin</p>"""

		send_mail(
			'Django Magic Link',
			html_message,
			'projectoriented34@yahoo.com',
			[email],
			fail_silently=False,
			html_message=html_message
		)
		return render(request, "authentication/login.html", {"message":"Please check your email for magic link."})
	return render(request, "authentication/login.html")

def confirmation(request, token):
	email = base64.b64decode(token.encode('utf-8')).decode('utf-8')
	user = User.objects.get(email=email)
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	auth_login(request, user)
	if user.is_authenticated:
		response = HttpResponse("You have been authenticated! <a href=\"/visits/\">Click</a> to see the number of visits")
		if not 'visits' in request.COOKIES:
			response.set_cookie('visits', 1)
		else:
			response.set_cookie('visits', int(request.COOKIES['visits']) + 1)
		return response
	else:
		return HttpResponse("Authentication failed :(")



@login_required
def home(request):
	return render(request, 'authentication/index.html', {'greeting': 'Welcome to Home page!'})

@login_required
def visits(request):
	return render(request, 'authentication/visits.html', {'visits': f"Number of magic url visits: {request.COOKIES['visits']}"})