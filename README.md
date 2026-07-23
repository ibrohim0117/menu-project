# 🍽 Menu & Order — Monorepo

Restoran uchun menu va buyurtmalarni boshqarish tizimi. Loyiha uchta qismdan iborat:

```
menu_drf/
├── backend/          # Django REST Framework API
├── frontend/         # Veb frontend (HTML/JS)
├── mobile/           # React Native (Expo) ilova
├── .gitignore        # Butun loyiha uchun umumiy gitignore
├── demb.md           # Vazifa shartlari (texnik topshiriq)
└── README.md         # Shu fayl
```

---

## 🔧 Backend (Django REST Framework)

Joylashuv: [backend/](backend/)

```
backend/
├── apps/             # Asosiy ilova (models, views, serializer, urls, filters)
├── root/             # Loyiha sozlamalari (settings, urls, wsgi, asgi)
├── media/            # Yuklangan fayllar (avatar, images) — gitignore'da
├── venv/             # Virtual muhit — gitignore'da
├── db.sqlite3        # Baza — gitignore'da
├── manage.py
└── requirements.txt
```

### Ishga tushirish

```bash
cd backend

# Virtual muhitni yoqish
source venv/bin/activate

# (Birinchi marta yoki paketlar yangilanganda)
pip install -r requirements.txt

# Migratsiyalar
python manage.py migrate

# Server
python manage.py runserver
```

Server: `http://127.0.0.1:8000`

### Hujjatlar

| Manzil | Tavsif |
|---|---|
| `/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI schema |
| `/admin/` | Django admin |

### Asosiy endpointlar

Barchasi `/api/` prefiksi bilan. Autentifikatsiya — **JWT** (`Authorization: Bearer <token>`).

**Auth va profil**
- `POST /api/auth/register/` — ro'yxatdan o'tish
- `POST /api/auth/login/` — token olish
- `POST /api/auth/refresh/` — tokenni yangilash
- `GET  /api/me/` — profil ma'lumotlari
- `PATCH /api/me/update/` — profilni yangilash

**Kategoriyalar**
- `GET|POST /api/categories/`
- `GET|PUT|PATCH|DELETE /api/categories/<id>/`

**Mahsulotlar**
- `GET|POST /api/products/`
- `GET|PUT|PATCH|DELETE /api/products/<id>/`

**Buyurtmalar**
- `GET|POST /api/orders/`
- `GET|PUT|PATCH|DELETE /api/orders/<id>/`
- `GET|POST /api/order-itemss/`
- `GET|PUT|PATCH|DELETE /api/order-items/<id>/`

**Savatcha**
- `GET  /api/carts/` — savatchadagi mahsulotlar
- `POST /api/cart-create/` — savatchaga qo'shish
- `DELETE /api/cart-remove/<id>/` — savatchadan o'chirish

---

## 🌐 Frontend (veb)

Joylashuv: [frontend/](frontend/)

Statik HTML sahifalar: `index.html`, `auth.html`, `carts.html`, `order.html`, `orders.html`, `profile.html`, `settings.html`.

API bazaviy manzil: `http://127.0.0.1:8000/api`

### Ishga tushirish

Backend ishlab turgan holda, oddiy statik server yetarli:

```bash
cd frontend
python3 -m http.server 3000
```

Ochish: `http://localhost:3000`

> `root/settings.py` da `CORS_ALLOW_ALL_ORIGINS = True`, shuning uchun localhost'ning istalgan portidan so'rov yuborish mumkin.

---

## 📱 Mobile (React Native / Expo)

Joylashuv: [mobile/](mobile/)

Hozircha bo'sh — Expo loyihasi shu papka ichida yaratiladi:

```bash
npx create-expo-app@latest mobile
cd mobile
npx expo start
```

> Telefondan test qilishda `127.0.0.1` ishlamaydi — kompyuteringizning lokal IP manzilidan foydalaning (masalan `http://192.168.1.5:8000/api`).

---

## 📋 Texnik topshiriq

To'liq vazifa sharti: [demb.md](demb.md)
