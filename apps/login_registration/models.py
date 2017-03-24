from __future__ import unicode_literals
import bcrypt
import re

from django.db import models

class UserManager(models.Manager):
	def login(self, username, password):
		user_confirm = User.objects.filter(username=username)
		if user_confirm:
			for user in user_confirm:
				user_password = user.hash_password
				user_id = user.id
			password = password.encode('utf-8')
			user_password = user_password.encode('utf-8')
			if bcrypt.hashpw(password, user_password) == user_password:
				return (True, user_id)
			else:
				return (False, "Login error: invalid password")
		else:
			return (False, "Login error: no user with that username")

	def register(self, name, username, password, password_confirm, date_hired):
		errors = []
		username_exists = User.objects.filter(username=username)
		if len(name) < 3:
			errors.append("Registration error: Name must be 3 or more characters")
		if len(username) < 3:
			errors.append("Registration error: Username must be 3 or more characters")
		if username_exists:
			errors.append("Registration error: Username already in use")
		if len(password) < 8:
			errors.append("Registration error: Password must be 8 or more characters")
		if password != password_confirm:
			errors.append("Registration error: Passwords must match")
		if not date_hired:
			errors.append("Registration error: Must add date hired")

		password = password.encode('utf-8')
		hashed = bcrypt.hashpw(password, bcrypt.gensalt())

		if errors:
			return errors
		else:
			new_user = self.create(name=name, username=username, date_hired=date_hired, hash_password=hashed)
			return (True, new_user.id)

class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	hash_password = models.CharField(max_length = 255)
	date_hired = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

