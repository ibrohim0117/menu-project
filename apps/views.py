from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
    
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from .models import Category, MenuItem, Order, OrderItem, User, Cart
from .serializer import (
    CategoryListSerializer, 
    MenuItemListSerializer, 
    OrderItemListSerializer, 
    OrderListSerializer,
    RegisterSerializer, GetMeSerializer,
    UserUpdateSerializer, CartListSerializer,
    CartCreateSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ==============================================================================

@extend_schema(tags=['auth'])
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# ==============================================================================

@extend_schema(tags=['category'])
class CategoryListCreateApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

@extend_schema(tags=['category'])
class CategoryRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]


# ==============================================================================

@extend_schema(tags=['menu-item'])
class MenuItemListCreateApiView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemListSerializer
    # Global PAGE_SIZE=5 (settings.py > REST_FRAMEWORK) ishlatiladi

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = {
        'category': ['exact'],
        'is_available': ['exact'],
        'price': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
    

@extend_schema(tags=['menu-item'])
class MenuItemRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

# ==============================================================================

@extend_schema(tags=['orders'])
class OrderListCreateApiView(ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

@extend_schema(tags=['orders'])
class OrderRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'delivered' and not request.user.is_staff:
            raise ValidationError({"error": "Yetkazib berilgan buyurtmani o'zgartirib bo'lmaydi!"})
        return super().update(request, *args, **kwargs)

# ==============================================================================

@extend_schema(tags=['order-items'])
class OrderItemListCreateApiView(ListCreateAPIView):
    serializer_class = OrderItemListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


@extend_schema(tags=['order-items'])
class OrderItemRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__customer=self.request.user)


class GetMe(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetMeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user



class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

@extend_schema(tags=['cart'])
class CartListAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).all()



@extend_schema(tags=['cart'])
class CartCreateAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@extend_schema(tags=['cart'])
class CartRemoveApiView(DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


    
