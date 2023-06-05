from django.contrib import admin
from mainapp.models import(
    Category, Product, Size, Color, Cart, CartProduct
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Cart)
admin.site.register(CartProduct)