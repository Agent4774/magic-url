from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from sesame.utils import get_query_string, get_user
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


def login(request):
	if request.method == "POST":
		email 			= request.POST.get("emailId")
		user 			= User.objects.get(email=email)
		login_token 	= get_query_string(user)
		login_link 		= f"http://localhost:8000/confirmation/{login_token}"		
		html_message 	= f"""<p>Hi there,</p><p>Here is your <a href="{login_link}">magic link</a></p><p>Thanks,</p><p>Django Admin</p>"""

		send_mail(
			'Django Magic Link',
			html_message,
			'muenze7777@gmail.com',
			[email],
			fail_silently=False,
			html_message=html_message
		)
		return render(request, "authentication/login.html", {"message":"Please check your email for magic link."})
	return render(request, "authentication/login.html")

@login_required
def confirmation(request):
	user = get_user(request, update_last_login=False)
	response = HttpResponse('Congrats! You have logged in :)<br><a href="/visits/">Click</a> to check the number of <strtong>visits</strong>.<br><a href="/home/">Click</a> to go to <strtong>Home page</strong>.')
	if not 'visits' in request.COOKIES:
		response.set_cookie('visits', 1)
	else:
		response.set_cookie('visits', int(request.COOKIES['visits']) + 1)
	return response



@login_required
def home(request):
	return render(request, 'authentication/index.html', {'greeting': 'Welcome to Home page!'})

@login_required
def visits(request):
	return render(request, 'authentication/visits.html', {'visits': f"Number of magic url visits: {request.COOKIES['visits']}"})