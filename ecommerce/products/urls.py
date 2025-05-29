from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('carts/<int:cart_id>/add_item/', AddItemToCart.as_view(), name='add-item-to-cart'),
    path('orders/create_from_cart/', CreateOrderFromCart.as_view(), name='create-order-from-cart'),
]
