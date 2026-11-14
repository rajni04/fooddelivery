from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Category)
admin.site.register(food)
admin.site.register(Order)
admin.site.register(OrderAddress)
admin.site.register(FoodTracking)
admin.site.register(PaymentDetails)
admin.site.register(Review)
admin.site.register(Wishlist)



# Register your models here.
