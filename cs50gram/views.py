from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

from .forms import UserRegisterForm, UserLoginForm, PostForm
from .models import User, Post


@login_required
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

				# Checks if the 'next' parameter is present through login_required decorator
				if 'next' in request.POST:
					return HttpResponseRedirect(request.POST.get('next'))
				# Else redirect the user to main page
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


@login_required
def add_post(request):
	"""Add post to the network"""

	if request.method == "POST":

		# Create a form instance and populate it with data from the request
		form = PostForm(request.POST, request.FILES)

		if form.is_valid():

			# Save a new Listing object from the form's data.
			post = form.save(commit=False)

			# Add the user to the form
			post.posted_by = request.user

			# Add the date_added to the form
			post.date_posted = datetime.datetime.now()

			post.save()

			return HttpResponseRedirect(reverse("index"))

		else:
			# If the form is not valid, render the template with errors
			return render(request, "cs50gram/add_post.html", {"form": form})

	form = PostForm()
	return render(request, "cs50gram/add_post.html", {"form": form})


@login_required
def explore(request):
	"""Renders all the posts on the network"""

	# Displays the post showing the newest first
	posts = Post.objects.all().order_by("date_posted").reverse()

	return render(request, "cs50gram/explore.html", {"posts": posts})


@csrf_exempt
@login_required
def like_post(request):
	"""Updates the like post in the database and the like_post API"""

	if request.method == "POST":

		# Gets the form data from the js
		post_id = request.POST.get('id')
		is_liked = request.POST.get('is_liked')

		try:
			post = Post.objects.get(id=post_id)
			if is_liked == 'no':
				post.like.add(request.user)
				is_liked = 'yes'
			elif is_liked == 'yes':
				post.like.remove(request.user)
				is_liked = 'no'

			post.save()

			return JsonResponse({'like_count': post.like.count(), 'is_liked': is_liked, "status": 201})
        
		except:
			return JsonResponse({'error': "Post not found", "status": 404})
            
	return JsonResponse({}, status=400)