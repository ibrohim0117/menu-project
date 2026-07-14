import random
from django.db import models
from django.utils.text import slugify

# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='avatar/', blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        while MenuItem.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}_{random.randint(0, 999999)}"
        return super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('preparing', 'Tayyorlanmoqda'),
        ('delivered', 'Yetkazib berildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='my_order'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    @property
    def total_price(self):
        jami_summa = 0
        for i in self.items.all():
            jami_summa += i.menu_price * i.quantity
        return jami_summa


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    menu_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, editable=False)


    def save(self, *args, **kwargs):
        if not self.menu_price:
            self.menu_price = self.menu_item.price
        return super().save(*args, **kwargs)



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_carts')
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='menu_cart')

    def __str__(self):
        return f"{self.user.username} --- {self.menu.name}"
