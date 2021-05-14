from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
import datetime

from .forms import UserRegisterForm, UserLoginForm, PostForm, ProfileForm
from .models import User, Post, Comment, Profile


@login_required
def index(request):

	# Displays the posts of the user followings and the current user
	followings = Profile.objects.get(user=request.user).followings.all()

	posts = Post.objects.filter(Q(posted_by__in=followings) | Q(posted_by=request.user)).order_by("date_posted").reverse()

	return render(request, "cs50gram/index.html", {"posts": posts})


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

	# Checks if the user is already authenticated
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse("index"))

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

	# Checks if the user is already authenticated
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse("index"))

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


@login_required
def profile(request, username):
	"""Shows the profile of every user"""

	# Gets the user profile based on the username
	profile = Profile.objects.get(user__username=username)

	return render(request, "cs50gram/profile.html", {"profile": profile})


@login_required
def edit_profile(request):
	
	profile = Profile.objects.get(user=request.user)

	if request.method == "POST":

		form = ProfileForm(request.POST, instance=profile)

		if form.is_valid():
			form.save()

			# Gets the field values from the request
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]

			user = User.objects.get(pk=request.user.id)

			user.first_name = first_name
			user.last_name = last_name

			user.save()

			return HttpResponseRedirect(reverse("profile", args=[profile.user.username]))


		else:
			# If the form is not valid, render the template with errors
			return render(request, "cs50gram/edit_profile.html", {"form": form})

	# Load the profile form pre-populated with initial values
	initial = {
		"first_name": profile.user.first_name,
		"last_name": profile.user.last_name,
		"birthdate": profile.birthdate,
		"gender": profile.gender,
		"bio": profile.bio
	}
	form = ProfileForm(initial=initial)
	return render(request, "cs50gram/edit_profile.html", {"form": form})


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
def load_comments(request, keyword, post_id):
	"""Returns the comments to index.js"""

	try:

		post = Post.objects.get(pk=post_id)
		response = []
		if keyword == "comments":
			# Filter comments to be returned based on post id
			response = list(Comment.objects.filter(post=post).values("comment", "commented_by__username"))
		
		elif keyword == "likes":
			# Return all the user who liked the post 
			response = list(post.like.all().values("username"))

		return JsonResponse({"keyword": keyword, "response": response})
		
	except:
		return JsonResponse({"error": "Post not found", "status": 404})


@csrf_exempt
@login_required
def follow(request):
	"""Updates the followings in the database"""

	if request.method == "POST":

		# Gets the form data from the js
		user = request.POST.get("user")
		keyword = request.POST.get("keyword")

		# Gets the user profile to be followed based on the username
		profile = Profile.objects.get(user__username=user).user

		try:
			
			if keyword == "Follow":
				# Follow the user and reverse the keyword
				current_user = Profile.objects.get(user=request.user)
				current_user.followings.add(profile)
				keyword = "Unfollow"
			elif keyword == "Unfollow":
				# Unfollow the user and reverse the keyword
				current_user = Profile.objects.get(user=request.user)
				current_user.followings.remove(profile)
				keyword = "Follow"

			return JsonResponse({"followers": profile.followers.all().count(), "keyword": keyword})

		except:
			return JsonResponse({"error": "User not found", "status": 404})


@csrf_exempt
@login_required
def followings(request, username, keyword):
	"""Fetches the followers of a user and send them as json"""

	try:
		profile = Profile.objects.get(user__username=username)

		response = []
		response_count = None

		if keyword == "followings":
			response = list(profile.followings.all().values("username"))
			response_count = profile.followings.all().count()
		elif keyword == "followers":
			followers = profile.user.followers.all()
			response_count = profile.user.followers.all().count()
			for follower in followers:
				response.append({"username": follower.user.username})

		return JsonResponse({"response": response, "response_count": response_count})

	except:
		return JsonResponse({"error": "User not found", "status": 404})