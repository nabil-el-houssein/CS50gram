from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	pass

	# Creates a Profile instance once a user is created
	def save(self, *args, **kwargs):
		created = not self.pk
		super(User, self).save(*args, **kwargs)
		if created:
			Profile.objects.create(user=self)


class Post(models.Model):
	"""Tracks the posts on the network"""

	posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
	image = models.ImageField(upload_to="posts/")
	caption = models.CharField(max_length=255, null=True, blank=True)
	like = models.ManyToManyField(User, blank=True, related_name="liked")
	date_posted = models.DateTimeField()


class Comment(models.Model):
	"""Tracks the comments on each post"""

	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.CharField(max_length=128)


class Profile(models.Model):
	"""Tracks the profile of each user"""

	GENDER = (
			("m", "Male"),
			("f", "Female"),
			("p", "Prefer Not To Say"),
		)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="profile-pics/", default="default_profile_pic.jpg")
	followings = models.ManyToManyField(User, blank=True, related_name="followers")
	gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
	birthdate = models.DateField(blank=True, null=True)
	bio = models.CharField(max_length=1024, null=True, blank=True)

	# Change the way the object is presented in the admin site
	def __str__(self):
		return f"{self.user}"

	# Removes old photo if found and it's not the default one
	def save(self, *args, **kwargs):
		try:
			this = Profile.objects.get(id=self.id)
			if this.profile_pic != self.profile_pic and this.profile_pic.name != "default_profile_pic.jpg":
				this.profile_pic.delete(save=False)
		except:
			pass	# when new photo then we do nothing, normal case
		super().save(*args, **kwargs)