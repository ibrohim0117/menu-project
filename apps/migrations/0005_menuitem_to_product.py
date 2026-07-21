from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    MenuItem -> Product qayta nomlash, Category ierarxiyasi (parent) va
    do'kon uchun kengaytirilgan mahsulot maydonlari.
    """

    dependencies = [
        ('apps', '0004_alter_order_order_number'),
    ]

    operations = [
        # ---------- 1. Model va maydon nomlarini o'zgartirish ----------
        migrations.RenameModel(old_name='MenuItem', new_name='Product'),
        migrations.RenameField(model_name='product', old_name='is_available', new_name='is_active'),
        migrations.RenameField(model_name='orderitem', old_name='menu_item', new_name='product'),
        migrations.RenameField(model_name='orderitem', old_name='menu_price', new_name='price'),
        migrations.RenameField(model_name='cart', old_name='menu', new_name='product'),

        # ---------- 2. Category ierarxiyasi ----------
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children', to='apps.category',
            ),
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),

        # ---------- 3. Product: yangi maydonlar ----------
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(
                blank=True, null=True, decimal_places=2, max_digits=12,
                help_text="Chegirma narxi. Bo'sh bo'lsa chegirma yo'q.",
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(
                blank=True, default='', max_length=50, unique=True,
                help_text="Artikul — bo'sh qoldirilsa avtomatik yaratiladi",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, null=True, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(
                default='dona', max_length=10,
                choices=[
                    ('dona', 'Dona'), ('kg', 'Kilogramm'), ('litr', 'Litr'),
                    ('metr', 'Metr'), ('m2', 'Kvadrat metr'),
                    ('quti', 'Quti'), ('paket', 'Paket'),
                ],
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0, help_text='Ombordagi mavjud soni'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(
                blank=True, null=True, decimal_places=3, max_digits=8,
                help_text="Og'irligi (kg)",
            ),
        ),

        # ---------- 4. Mavjud maydonlarni moslashtirish ----------
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='products', to='apps.category',
            ),
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),

        # ---------- 5. OrderItem / Cart bog'lanishlari ----------
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='order_items', to='apps.product',
            ),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=12),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='product_cart', to='apps.product',
            ),
        ),
    ]
