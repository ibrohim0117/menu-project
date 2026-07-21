from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, User, Cart

# ==============================================================================
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ==============================================================================
class CategoryListSerializer(ModelSerializer):
    """Kategoriya. `children` — shu bo'lim ostidagi kategoriyalar nomlari."""
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children', 'product_count', 'created_at']

    def get_children(self, obj):
        return [{'id': c.id, 'name': c.name} for c in obj.children.all()]

    def get_product_count(self, obj):
        return obj.products.count()


class ProductListSerializer(ModelSerializer):
    """Mahsulot. `final_price` — chegirma bo'lsa chegirma narxi."""
    final_price = serializers.ReadOnlyField()
    in_stock = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'category_name', 'image',
            'price', 'discount_price', 'final_price',
            'sku', 'barcode', 'brand', 'unit', 'stock', 'in_stock', 'weight',
            'is_active', 'created_at',
        ]
        read_only_fields = ['slug', 'final_price', 'in_stock', 'category_name']


class OrderItemListSerializer(ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ['price', 'order', 'product_name']


class OrderListSerializer(ModelSerializer):
    items = OrderItemListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'total_price', 'items', 'order_number']
        read_only_fields = ['customer', 'status', 'total_price', 'order_number']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        for item_data in items_data:
            product = item_data['product']
            if not product.is_active:
                raise serializers.ValidationError(
                    {"error": f"'{product.name}' mahsuloti sotuvda emas! Buyurtma berib bo'lmaydi."}
                )
            if product.stock < item_data.get('quantity', 1):
                raise serializers.ValidationError(
                    {"error": f"'{product.name}' omborda yetarli emas (mavjud: {product.stock} {product.unit})."}
                )

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            # buyurtma berilgach ombordan ayiramiz
            product = item_data['product']
            product.stock = max(0, product.stock - item_data.get('quantity', 1))
            product.save(update_fields=['stock'])
        return order


class OrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', ]


class GetMeSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'telegram', 'instagram', 'image'
        ]


class CartListSerializer(ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product']


class CartCreateSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'product']
        read_only_fields = ['user']
