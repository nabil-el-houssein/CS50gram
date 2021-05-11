from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("add-post", views.add_post, name="add-post"),
	path("explore", views.explore, name="explore"),

	path("login", views.login_view, name="login"),
	path("register", views.register, name="register"),
	path("logout", views.logout_view, name="logout"),

	# APIs
	path("like_post/", views.like_post),
]