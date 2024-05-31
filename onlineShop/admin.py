from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Store)
admin.site.register(User)
admin.site.register(Brand)
# admin.site.register(Accesories)
# admin.site.register(Accesories_Pro)
admin.site.register(Offer)
admin.site.register(Product)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(Order)
admin.site.register(OrderedItem)