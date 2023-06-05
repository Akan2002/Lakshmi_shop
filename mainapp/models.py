from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=127)
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.ManyToManyField('Size', verbose_name='Размер товара', related_name='product_sizes')
    color = models.ManyToManyField('Color', verbose_name='Цвет товара', related_name='product_colors')
    is_draft = models.BooleanField(default=False)

    @property
    def final_price(self):
        if self.discount > 0:
            return round(self.price - (self.price * self.discount / 100), 2)
        return self.price
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Cart(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in cart {self.cart.id}"