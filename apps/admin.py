from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart

# 1. Kategoriya admini (ierarxik: bo'lim > kategoriya)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']

# 2. Mahsulotlar admini
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discount_price', 'stock', 'unit', 'is_active']
    list_filter = ['category', 'is_active', 'unit']
    search_fields = ['name', 'sku', 'barcode', 'brand']
    list_editable = ['price', 'discount_price', 'stock', 'is_active']  # Ro'yxatdan turib o'zgartirish
    readonly_fields = ['slug', 'created_at']

# 3. Buyurtma ichidagi mahsulotlarni ko'rsatish (Inline)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Yangi buyurtma qo'shayotganda standart nechta qator chiqishi
    readonly_fields = ['price']

# 4. Buyurtmalar admini
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer__username']
    inlines = [OrderItemInline]  # Buyurtma ichida unga tegishli mahsulotlarni ko'rsatadi

# 5. Savatcha admini
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    search_fields = ['user__username', 'product__name']
