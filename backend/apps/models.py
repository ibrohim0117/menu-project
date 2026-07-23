import random
from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='avatar/', blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    """
    Ierarxik kategoriya: parent bo'sh bo'lsa — bu bo'lim (masalan "Oziq-ovqat"),
    parent to'ldirilgan bo'lsa — shu bo'lim ostidagi kategoriya ("Sut mahsulotlari").
    """
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    @property
    def is_root(self):
        """Bo'limmi (ota-onasi yo'q)?"""
        return self.parent_id is None


class Product(models.Model):
    UNIT_CHOICES = [
        ('dona', 'Dona'),
        ('kg', 'Kilogramm'),
        ('litr', 'Litr'),
        ('metr', 'Metr'),
        ('m2', 'Kvadrat metr'),
        ('quti', 'Quti'),
        ('paket', 'Paket'),
    ]

    # --- Asosiy ---
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    # --- Narx ---
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="Chegirma narxi. Bo'sh bo'lsa chegirma yo'q."
    )

    # --- Ombor / identifikatsiya ---
    sku = models.CharField(
        max_length=50, unique=True, blank=True,
        help_text="Artikul — bo'sh qoldirilsa avtomatik yaratiladi"
    )
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='dona')
    stock = models.PositiveIntegerField(default=0, help_text="Ombordagi mavjud soni")
    weight = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True,
        help_text="Og'irligi (kg)"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'mahsulot'
            slug = base
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}_{random.randint(0, 999999)}"
            self.slug = slug

        if not self.sku:
            sku = f"SKU-{random.randint(100000, 999999)}"
            while Product.objects.filter(sku=sku).exclude(pk=self.pk).exists():
                sku = f"SKU-{random.randint(100000, 999999)}"
            self.sku = sku

        return super().save(*args, **kwargs)

    @property
    def final_price(self):
        """Chegirma bo'lsa chegirma narxi, aks holda asosiy narx."""
        return self.discount_price if self.discount_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0


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

    order_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            number = f"#{random.randint(1, 99999)}"
            while Order.objects.filter(order_number=number).exists():
                number = f"#{random.randint(1, 99999)}"
            self.order_number = number
        return super().save(*args, **kwargs)

    @property
    def total_price(self):
        jami_summa = 0
        for i in self.items.all():
            jami_summa += i.price * i.quantity
        return jami_summa


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, editable=False)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.final_price
        return super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')

    def __str__(self):
        return f"{self.user.username} --- {self.product.name}"
