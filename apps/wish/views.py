from django.shortcuts import render, redirect, reverse
from .models import Item, User
from django.contrib import messages

def index(request):
	if 'user_id' in request.session:
		user = User.objects.get(id = request.session['user_id'])
		user_wishlist = user.wishlists.all()
		items_not_in_wishlist = Item.objects.not_in_wishlist(user)
		context = {
			'user': user,
			'user_wishlist': user_wishlist,
			'items_not_in_wishlist': items_not_in_wishlist
			}
		return render(request, 'wish/index.html', context)
	else:
		return render(request, 'wish/authfail.html')

def display_item(request, item_id):
	if 'user_id' in request.session:
		item = Item.objects.get(id = item_id)
		context = {
			'item': item
		}
		return render(request, 'wish/display_item.html', context)
	else:
		return render(request, 'wish/authfail.html')

def create(request):
	if 'user_id' in request.session:
		return render(request, 'wish/new_item.html')
	else:
		return render(request, 'wish/authfail.html')

def add_item(request):
	if request.method == 'POST':
		model_response = Item.objects.create_item(request.POST, request.session['user_id'])
		if model_response[0]:
			return redirect(reverse('dashboard:index'))
		else:
			messages.error(request, model_response[1])
			return redirect(reverse('wish_items:create'))
	else:
		return render(request, 'wish/authfail.html')

def add_to_wishlist(request, item_id):
	if request.method == 'POST':
		model_response = Item.objects.add_to_wishlist(item_id, request.session['user_id'])
		return redirect(reverse('dashboard:index'))
	else:
		return render(request, 'wish/authfail.html')

def remove_from_wishlist(request, item_id):
	if request.method == 'POST':
		model_reponse = Item.objects.remove_from_wishlist(item_id, request.session['user_id'])
		return redirect(reverse('dashboard:index'))
	else:
		return render(request, 'wish/authfail.html')

def destroy_item(request, item_id):
	if request.method == 'POST':
		model_reponse = Item.objects.destroy_item(item_id)
		return redirect(reverse('dashboard:index'))
	else:
		return render(request, 'wish/authfail.html')
