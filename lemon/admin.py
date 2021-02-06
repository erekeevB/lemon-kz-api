from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)

admin.site.register(Item)

admin.site.register(ItemImg)

admin.site.register(Sex)

admin.site.register(Review)

admin.site.register(CartItem)

admin.site.register(FavouriteItem)

admin.site.register(Brand)