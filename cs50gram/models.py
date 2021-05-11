from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	pass


class Post(models.Model):
	"""Tracks the posts on the network"""

	posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField()
	caption = models.CharField(max_length=255, null=True, blank=True)
	like = models.ManyToManyField(User, blank=True, related_name="liked")
	date_posted = models.DateTimeField()