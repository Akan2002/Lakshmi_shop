from rest_framework.viewsets import ModelViewSet
from mainapp.models import Category, Product, Cart, CartProduct
from mainapp.serializers import(
    UserSerializer, CategorySerializer, ProductSerializer, CartSerializer, 
    CartProductSerializer, RegistrationSerializer, AuthenticationSerializer
)

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import(
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
)

from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (
        filters.SearchFilter,
    )

    search_fields = (
        'name', 'category_name',
    )

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_fields = (
        'category',
    )

    search_fields = (
        'name', 'category__name',
    )

    ordering_fields = (
        'id', 'price', 'discount',
    )

    @action(methods=['get', ], detail=False)
    def get_discount_product(self, request, *args, **kwargs):
        products = Product.objects.filter(discount__gt=0)
        serializers = ProductSerializer(products, many=True).data
        return Response(serializers)
    
class CartView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartProductView(ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return Response(
                {'message': 'Пользователь с таким именем сущуствует'},
                status=HTTP_403_FORBIDDEN
            )
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        token = Token.objects.create(user=user)
        return Response({'token': token.key}, HTTP_201_CREATED)
    
class AuthenticationView(APIView):
    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            if check_password(password, user.password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, HTTP_200_OK)
            return Response({'error': 'Пароль не верный'}, HTTP_400_BAD_REQUEST)
        return Response({'error': 'Пользователь не существует'}, HTTP_400_BAD_REQUEST)