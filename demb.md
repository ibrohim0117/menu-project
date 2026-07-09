# 🍽 Restaurant Menu & Order API — Amaliy Vazifa

**Mavzu:** Django REST Framework (DRF) | CRUD · Filter · Permission · JWT Auth
**Daraja:** O'rta
**Tavsiya etilgan vaqt:** 1-2 kun

---

## 🎯 Vazifa maqsadi

Restoran uchun menu va buyurtmalarni boshqaradigan REST API yarating. API quyidagilarni qo'llab-quvvatlashi kerak:

- Modellar bilan ishlash (CRUD)
- Ma'lumotlarni filterlash va qidirish
- Foydalanuvchi rollariga qarab ruxsatlar (permissions)
- **Faqat JWT (JSON Web Token) orqali autentifikatsiya** — Basic auth ishlatilmaydi

---

## 🧱 1. Modellar (Models)

Quyidagi modellarni yarating:

### `Category`
| Field | Type | Izoh |
|-------|------|------|
| `name` | CharField | unique, max_length=100 |
| `created_at` | DateTimeField | auto_now_add |

### `MenuItem`
| Field | Type | Izoh |
|-------|------|------|
| `name` | CharField | max_length=200 |
| `description` | TextField | blank=True |
| `price` | DecimalField | max_digits=8, decimal_places=2 |
| `category` | ForeignKey → Category | related_name="items" |
| `is_available` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add |

### `Order`
| Field | Type | Izoh |
|-------|------|------|
| `customer` | ForeignKey → User | buyurtma bergan foydalanuvchi |
| `status` | CharField | choices: `pending`, `preparing`, `delivered`, `cancelled` (default=`pending`) |
| `created_at` | DateTimeField | auto_now_add |

### `OrderItem`
| Field | Type | Izoh |
|-------|------|------|
| `order` | ForeignKey → Order | related_name="items" |
| `menu_item` | ForeignKey → MenuItem | |
| `quantity` | PositiveIntegerField | default=1 |

> 💡 **Bonus:** `Order` modeliga `total_price` ni hisoblaydigan property yoki method qo'shing (har bir OrderItem narxi × quantity yig'indisi).

---

## 🔌 2. Endpointlar (CRUD)

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/categories/` | Barcha kategoriyalar |
| POST | `/api/categories/` | Yangi kategoriya (faqat admin) |
| GET/PUT/PATCH/DELETE | `/api/categories/{id}/` | Bitta kategoriya |
| GET | `/api/menu-items/` | Barcha taomlar |
| POST | `/api/menu-items/` | Yangi taom (faqat admin) |
| GET/PUT/PATCH/DELETE | `/api/menu-items/{id}/` | Bitta taom |
| GET | `/api/orders/` | Buyurtmalar (faqat o'ziniki) |
| POST | `/api/orders/` | Yangi buyurtma |
| GET/PATCH/DELETE | `/api/orders/{id}/` | Bitta buyurtma |


---

## 🔐 3. Autentifikatsiya — faqat JWT

`djangorestframework-simplejwt` kutubxonasidan foydalaning.

```bash
pip install djangorestframework-simplejwt
```

`settings.py`:
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

Quyidagi auth endpointlari bo'lishi shart:

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| POST | `/api/auth/register/` | Ro'yxatdan o'tish |
| POST | `/api/auth/login/` | `access` va `refresh` token olish |
| POST | `/api/auth/refresh/` | `access` token ni yangilash |

> ❗️ `BasicAuthentication` va `SessionAuthentication` ni **ishlatmang**. Faqat JWT.

---

## 🛡 4. Ruxsatlar (Permissions)

| Resurs | Ruxsat qoidasi |
|--------|----------------|
| `Category`, `MenuItem` ko'rish (GET) | Hamma ko'ra oladi (authenticated bo'lmasa ham — `AllowAny` GET uchun) |
| `Category`, `MenuItem` yaratish/o'zgartirish/o'chirish | Faqat **admin (staff)** |
| `Order` yaratish | Faqat **login qilgan** foydalanuvchi |
| `Order` ko'rish/o'zgartirish | Foydalanuvchi **faqat o'z buyurtmalarini** ko'ra/o'zgartira oladi |
| Admin | Barcha buyurtmalarni ko'ra oladi |

> 💡 `IsAuthenticatedOrReadOnly`, `IsAdminUser` dan foydalaning va o'z **custom permission** (masalan `IsOwnerOrAdmin`) ni yozing.

---

## 🔍 5. Filter, Qidirish va Saralash

`django-filter` o'rnating:
```bash
pip install django-filter
```

**MenuItem** uchun:
- Filter: `category`, `is_available`, narx oralig'i (`price_min`, `price_max`)
- Qidirish (`search`): `name`, `description` bo'yicha
- Saralash (`ordering`): `price`, `created_at` bo'yicha

**Order** uchun:
- Filter: status bo'yicha
Misol so'rovlar:
```
GET /api/menu-items/?category=2&is_available=true
GET /api/menu-items/?search=lavash&ordering=-price
GET /api/menu-items/?price_min=20000&price_max=50000
GET /api/orders/?status=pending
```

---

## ✅ 6. Topshirish talablari

1. Loyiha GitHub repositoriyada bo'lsin
2. `requirements.txt` mavjud bo'lsin
3. Migratsiyalar to'g'ri ishlasin
5. Postman/DRF-spektecular

---

## 🏆 Baholash mezonlari (100 ball)

| Bo'lim | Ball |
|--------|------|
| Modellar to'g'ri tuzilgan | 15 |
| CRUD endpointlar ishlaydi | 25 |
| JWT auth (register/login/refresh) | 20 |
| Permissions to'g'ri ishlaydi | 20 |
| Filter / search / ordering | 15 |
| README + kod tozaligi | 5 |
| **Bonus:** `total_price`, custom permission, Postman collection | +10 |

---

## 💡 Bonus topshiriqlar (ixtiyoriy)

- `Order` yaratishda bitta so'rovda bir nechta `OrderItem` qo'shish (nested serializer)
- Taom mavjud emas (`is_available=False`) bo'lsa, uni buyurtmaga qo'shishni taqiqlang
- Pagination qo'shing (sahifalash)
- `Order` statusi `delivered` bo'lgach uni o'zgartirib bo'lmaydigan qiling

---

Omad! 🚀