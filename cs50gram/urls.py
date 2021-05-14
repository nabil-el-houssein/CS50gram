from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("add-post", views.add_post, name="add-post"),
	path("explore", views.explore, name="explore"),
	path("profile/<str:username>", views.profile, name="profile"),
	path("accounts/edit-profile", views.edit_profile, name="edit-profile"),

	path("login", views.login_view, name="login"),
	path("register", views.register, name="register"),
	path("logout", views.logout_view, name="logout"),

	# APIs
	path("like_post/", views.like_post),
	path("add_comment/", views.add_comment),
	path("post/<str:keyword>/<int:post_id>", views.load_comments),
	path("follow/", views.follow),
	path("user/<str:username>/<str:keyword>", views.followings),
]