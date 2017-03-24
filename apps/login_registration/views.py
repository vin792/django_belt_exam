from django.shortcuts import render, redirect, reverse
import bcrypt
from . models import User, UserManager
from django.contrib import messages
from datetime import datetime 

def index(request):
	
	print User.objects.all()

	if 'user_id' in request.session:
		request.session.pop('user_id')

	return render(request, 'login_registration/index.html')

def register(request):
	if request.method == "POST":

		register_outcome = User.objects.register(request.POST['name'],request.POST['username'],request.POST['password'],request.POST['password_confirm'],request.POST['date_hired'])

		if isinstance(register_outcome, tuple):
			request.session['user_id'] = register_outcome[1]
			return redirect(reverse('dashboard:index')) 
		else:
			for error_message in register_outcome:
				messages.error(request, error_message, extra_tags='register')
			return redirect(reverse('login:index'))

def login(request):
	if request.method == "POST":
		user_login_result = User.objects.login(request.POST['username'], request.POST['password'])
		if user_login_result[0]:
			request.session['user_id'] = user_login_result[1]
			return redirect(reverse('dashboard:index'))
		else:
			messages.error(request, user_login_result[1], extra_tags='login')
			return redirect(reverse('login:index'))
