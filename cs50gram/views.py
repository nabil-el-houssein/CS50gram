from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import datetime

from .forms import UserRegisterForm, UserLoginForm, PostForm
from .models import User, Post, Comment


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
	"""Updates the post like in the database and the like_post API"""

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
	
	# If the request is GET send a bad request (status 400)
	return JsonResponse({}, status=400)


@csrf_exempt
@login_required
def add_comment(request):
	"""Updates the post comment in the database and the add_comment API"""

	if request.method == "POST":

		# Gets the form data from the js
		post_id = request.POST.get('id')
		comment = request.POST.get('comment')

		try:
			# Gets the post based on the id
			post = Post.objects.get(id=post_id)

			# Creates a new comment
			post_comment = Comment.objects.create(post=post, commented_by=request.user, comment=comment)

			# Gets the user who commented
			user = f"{request.user} "

			# Return the new number of comments and the user who added the comment
			return JsonResponse({"comment_count": post.comments.all().count(), "commented_by": user, "status": 201})
		
		except:
			return JsonResponse({"error": "Post not found", "status": 404})
	
	# If the request is GET send a bad request (status 400)
	return JsonResponse({}, status=400)


@login_required
def load_comments(request, post_id):
	"""Returns the comments to index.js"""

	try:
		# Filter comments returned based on post id
		post = Post.objects.get(pk=post_id)

		comments = list(Comment.objects.filter(post=post).values("comment", "commented_by__username"))

		return JsonResponse({"comments": comments})
		
	except:
		return JsonResponse({"error": "Post not found", "status": 404})


@csrf_exempt
@login_required
def delete_post(request):
	"""Delete a Post"""

	if request.method == "POST":
		# Gets the form data from the js
		post_id = request.POST.get("id")

		try:
			post = Post.objects.get(pk=post_id)

			# Check if the logged in user owns the post
			if post.posted_by == request.user:
				post.delete()
				return JsonResponse({"status": 201})
			else:
				return JsonResponse({"error": "Permission Denied", "status": 403})
		except:
			return JsonResponse({"error": "Post not found", "status": 404})

	# If the request is GET send a bad request (status 400)
	return JsonResponse({}, status=400)