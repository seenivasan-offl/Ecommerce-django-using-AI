from django.contrib import admin
from .models import Product, UserInteraction, Order

admin.site.register(Product)
admin.site.register(UserInteraction)
admin.site.register(Order)
