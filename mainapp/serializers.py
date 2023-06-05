from rest_framework import serializers

from mainapp.models import(
    Category, Product, Size, Color, Cart, CartProduct, 
)

from mainapp.listing_serializer import ColorListingField, SizeListingField

from django.contrib.auth import get_user_model

User = get_user_model()

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('id', 'cart', 'product', 'amount')

class CartSerializer(serializers.ModelSerializer):
    products = serializers.ListField(write_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'email', 'created_at', 'updated_at', 'products')

    def create(self, validated_data):
        emial = validated_data.get('emial')
        products = validated_data.get('products')
        cart = Cart.objects.create(emial=emial)

        for p in products:
            product = Product.objects.filter(id=p.get('product_id')).first()
            CartProduct.objects.create(
                cart=cart,
                product=product,
                amount=p.get('product_amount')
            )

            return cart

class ProductSerializer(serializers.ModelSerializer):
    size = SizeListingField(read_only=True, many=True)
    color = ColorListingField(read_only=True, many=True)
    class Meta:
        model = Product
        fields = (
            'id', 'category', 'name', 'description', 'price', 'discount', 
            'image', 'created_at', 'updated_at', 'size', 'color',
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'products')

class UserSerializer(serializers.ModelSerializer):
    carts = CartSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'carts')

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()