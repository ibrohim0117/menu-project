from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Cart

# 1. Kategoriya admini
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# 2. Menu elementlari admini
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']
    list_editable = ['price', 'is_available']  # Admin panelning o'zidan turib o'zgartirish uchun

# 3. Buyurtma ichidagi mahsulotlarni ko'rsatish (Inline)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Yangi buyurtma qo'shayotganda standart nechta qator chiqishi

# 4. Buyurtmalar admini
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']  # Agar user modeliga bog'langan bo'lsa
    inlines = [OrderItemInline]  # Buyurtma ichida unga tegishli mahsulotlarni ko'rsatadi


admin.site.register(Cart)