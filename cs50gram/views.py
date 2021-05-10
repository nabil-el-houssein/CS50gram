from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import UserRegisterForm, UserLoginForm
from .models import User

def index(request):
	return render(request, "cs50gram/index.html")


def register(request):
	"""Creates a new user and logs the user in"""

	if request.method == "POST":

		# Create a form instance and populate it with data from the request
		form = UserRegisterForm(request.POST)

		if form.is_valid():

			# Gets the field values from the request
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			email = form.cleaned_data["email"]
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]

			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.date_joined = datetime.datetime.now()

			user.save()

			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			# If the form is not valid, render the template with errors
			return render(request, "cs50gram/register.html", {"form": form})

	form = UserRegisterForm()
	return render(request, "cs50gram/register.html", {"form": form})


def login_view(request):
	"""Authenticates the user and logs the user in"""

	if request.method == "POST":

		# Create a form instance and populate it with data from the request
		form = UserLoginForm(request.POST)

		if form.is_valid():

			# Attempt to sign user in
			username = request.POST["username"]
			password = request.POST["password"] 

			user = authenticate(request, username=username, password=password)

			# Check if authentication successful
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse("index"))
			else:
				return render(request, "cs50gram/login.html", {
						"message": "Invalid username and/or password.",
						"form": form
					})
		else:
			# If the form is not valid, render the template with errors
			return render(request, "cs50gram/register.html", {"form": form})

	form = UserLoginForm()
	return render(request, "cs50gram/login.html", {"form": form})


def logout_view(request):
	"""Logs out the user"""

	logout(request)
	return HttpResponseRedirect(reverse("index"))