from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    CategoryListCreateApiView, CategoryRetrieveUpdateDestroyApiView,
    MenuItemListCreateApiView, MenuItemRetrieveUpdateDestroyApiView,
    OrderListCreateApiView, OrderRetrieveUpdateDestroyApiView,
    OrderItemRetrieveUpdateDestroyApiView, OrderItemListCreateApiView, 
    GetMe, UserUpdate, CartListAPIView, CartCreateAPIView,
    CartRemoveApiView
)

urlpatterns = [
    #Autentifikatsiya
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', GetMe.as_view(), name='me'),
    path('me/update/', UserUpdate.as_view(), name='me-update'),

    #Kategoriyalar
    path('categories/', CategoryListCreateApiView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyApiView.as_view(), name='category_detail'),

    #Taomlar menyusi
    path('menu-items/', MenuItemListCreateApiView.as_view(), name='menu_item_list_create'),
    path('menu-items/<int:pk>/', MenuItemRetrieveUpdateDestroyApiView.as_view(), name='menu_item_detail'),

    #Buyurtmalar
    path('orders/', OrderListCreateApiView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyApiView.as_view(), name='order_detail'),

    #Buyurtma elementlari
    path('order-itemss/', OrderItemListCreateApiView.as_view(), name='order_item_post'),
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyApiView.as_view(), name='order_item_detail'),

    #Savatcha
    path('carts/', CartListAPIView.as_view(), name='carts'),
    path('cart-create/', CartCreateAPIView.as_view(), name='cart-create'),
    path('cart-remove/<int:pk>/', CartRemoveApiView.as_view(), name='cart-remove'),
]