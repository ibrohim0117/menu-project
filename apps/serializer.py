from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Category, MenuItem, Order, OrderItem, User

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
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemListSerializer(ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderItemListSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['menu_price', 'order']

class OrderListSerializer(ModelSerializer):
    items = OrderItemListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'total_price', 'items']
        read_only_fields = ['customer', 'status', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        for item_data in items_data:
            menu_item = item_data['menu_item']
            if not menu_item.is_available:
                raise serializers.ValidationError(
                    {"error": f"'{menu_item.name}' taomi hozirda mavjud emas! Buyurtma berib bo'lmaydi."}
                )

        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class GetMeSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        # fields = []
        exclude = ['password', 'groups', 'user_permissions']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'telegram', 'instagram', 'image'
        ]