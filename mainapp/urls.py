from rest_framework.routers import DefaultRouter as DR
from django.urls import path

from mainapp.views import(
    UserView, CategoryView, ProductView, CartView, 
    CartProductView, RegistrationView, AuthenticationView, 
)

router = DR()

router.register('user', UserView)
router.register('category', CategoryView)
router.register('product', ProductView)
router.register('cart', CartView)
router.register('cartproduct', CartProductView)

urlpatterns = [
    path('reg/', RegistrationView.as_view()),
    path('auth/', AuthenticationView.as_view()),
]

urlpatterns += router.urls