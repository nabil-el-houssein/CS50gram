from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
import re

from .models import User


class UserRegisterForm(forms.ModelForm):

	# Overrides specific fields
	password = forms.CharField(widget=forms.PasswordInput())
	# Creates a field to confirm password
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ["first_name", "last_name", "email", "username", "password", "confirm_password"]

		# Add widgets to specific form fields 
		widgets = {
			"username": forms.TextInput(attrs={"autocomplete": "off"}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper()

		self.helper.form_method = "post"
		self.helper.form_action = 'register'

		self.helper.add_input(Submit("register", "Register", css_class='btn-primary btn-dark mx-auto'))

		self.helper.layout = Layout(
			Row(
				Column("first_name"),
				Column("last_name"),
			),
			"email",
			"username",
			"password",
			"confirm_password",
		)

		# Make fields required
		for field in ["first_name", "last_name", "email", "confirm_password"]:
			self.fields[field].required = True

		# Remove helptext in username
		self.fields["username"].help_text = None


	def clean(self):
		cleaned_data = super(UserRegisterForm, self).clean()

		username = cleaned_data.get("username")

		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		# Username allowed characters
		pattern = re.compile("^(?=.{4,25}$)(?![.])[a-zA-Z0-9._]+(?<![.])$")

		# Validates username length
		if len(username) < 4 or len(username) > 25:
			self.add_error("username", "Username must be between 4 and 25 characters.")

		# Checks if username starts or end with a period
		if username[0] == '.' or username[-1] == '.':
			self.add_error("username", "Username cannot start or end with a period.")

		# Checks username allowed characters
		elif pattern.search(username) is None:
			self.add_error("username", "Username can only contain alphanumeric, underscore and period.")

		# Checks password length
		if len(password) < 8:
			self.add_error("password", "Password must be at least 8 characters.")

		# Checks if passwords matches
		if password != confirm_password:
			self.add_error("password", "Passwords do not match")
			self.add_error("confirm_password", "Passwords do not match")

		return cleaned_data


class UserLoginForm(forms.Form):

	# Creates Form fields
	username= forms.CharField(widget=forms.TextInput())
	password= forms.CharField(widget=forms.PasswordInput())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper()

		self.helper.form_method = "post"
		self.helper.form_action = 'login'

		self.helper.add_input(Submit("login", "Login", css_class='btn-primary btn-dark'))