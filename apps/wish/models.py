from __future__ import unicode_literals
from ..login_registration.models import User

from django.db import models

class ItemManager(models.Manager):
	def create_item(self, postData, user_id):
		user = User.objects.get(id = user_id)
		error = ""
		if not postData['item_name']:
			error = "Item must have a name"
		elif len(postData['item_name']) <= 3:
			error = "Item name must be more than 3 characters long"

		if error:
			return (False, error)
		else:
			new_item = self.create(name=postData['item_name'], user=user)
			user.wishlists.add(new_item)
			return (True, "Item added")

	def not_in_wishlist(self, user):
		all_items = Item.objects.all()
		user_wishlist = user.wishlists.all()
		not_in_user_wishlist = []
		for item in all_items:
			if item not in user_wishlist:
				not_in_user_wishlist.append(item)
		return not_in_user_wishlist

	def add_to_wishlist(self, item_id, user_id):
		item = Item.objects.get(id = item_id)
		user = User.objects.get(id = user_id)
		user.wishlists.add(item)
		return(True, "Item added to wishlist")

	def remove_from_wishlist(self, item_id, user_id):
		item = Item.objects.get(id = item_id)
		user = User.objects.get(id = user_id)
		item.wishlists.remove(user)
		return(True, "Item removed from wishlist")

	def destroy_item(self, item_id):
		Item.objects.filter(id = item_id).delete()
		return(True, "Item deleted")

class Item(models.Model):
	name = models.CharField(max_length = 255)
	user = models.ForeignKey(User, related_name = "items")
	wishlists = models.ManyToManyField(User, related_name = "wishlists")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ItemManager()
		
