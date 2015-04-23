from django.contrib import admin
from .models import Customer, Product, Order, Payment

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Payment)

