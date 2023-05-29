from rest_framework import serializers

from mainapp.models import(
    Category, Product, Cart, CartProduct, 
)

from django.contrib.auth import get_user_model

User = get_user_model()

class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ('id', 'cart', 'product', 'amount')

class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'cart_products')

    def create(self, validated_data):
        user = validated_data.get('user')
        products = validated_data.get('products')
        cart = Cart.objects.create(user=user)

        for p in products:
            product = Product.objects.filter(id=p.get('product_id')).first()
            CartProduct.objects.create(
                cart=cart,
                product=product,
                amount=p.get('product_amount')
            )

            return cart
        
    def to_representation(self, instance):
        cart_products = instance.cart_products.all()
        result = [instance.user]
        for cp in cart_products:
            product = {
                'product_name': cp.product.name,
                'product_id': cp.product.id,
                'amount': cp.amount
            }
            result.append(product)

class ProductSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'name', 'description', 'price', 'discount',
            'image', 'created_at', 'updated_at', 'cart_products',
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