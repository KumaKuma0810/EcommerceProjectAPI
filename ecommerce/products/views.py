from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import *

class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    permissions_classes = [permissions.IsAdminInUser]


class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permissions_classes = [permissions.IsAdminInUser]


class OrderAdminViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

# ----------------------------------------------------

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    quearyset = Category.objects.all()
    serializer_class =CategorySerializer
    permissions_classes = [permissions.IsAllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    quearyset = Product.objects.all()
    serializer_class =ProductSerializer
    permissions_classes = [permissions.IsAllowAny]


class CartViewSet(viewset.ModelViewSet):
    quearyset = Product.objects.all()
    serializer_class =ProductSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)


class AddItemToCart(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        item, create = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            items.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CategorySerializer(cart).date, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)


class CreateOrderFromCart(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user = request.user)

