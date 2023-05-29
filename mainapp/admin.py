from django.contrib import admin
from mainapp.models import(
    Category, Product, Cart, CartProduct
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)