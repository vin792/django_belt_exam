from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<item_id>\d+)$', views.display_item, name='display_item'),
    url(r'^create$', views.create, name='create'),
    url(r'^additem$', views.add_item, name='add_item'),
    url(r'^addtowishlist/(?P<item_id>\d+)$', views.add_to_wishlist, name='add_to_wishlist'),
    url(r'^removefromwishlist/(?P<item_id>\d+)$', views.remove_from_wishlist, name='remove_from_wishlist'),
    url(r'^destroyitem/(?P<item_id>\d+)$', views.destroy_item, name='destroy_item'),
]
