# 🐍 Полный мануал по Python фреймворкам: Django, FastAPI, Flask и другие

## 📋 Содержание

1. [Введение в Python фреймворки](#введение-в-python-фреймворки)
2. [Django](#django)
3. [FastAPI](#fastapi)
4. [Flask](#flask)
5. [Pyramid](#pyramid)
6. [Tornado](#tornado)
7. [Sanic](#sanic)
8. [Quart](#quart)
9. [Практические примеры](#практические-примеры)
10. [Сравнение фреймворков](#сравнение-фреймворков)
11. [Лучшие практики](#лучшие-практики)

## Введение в Python фреймворки

`Python` фреймворки предоставляют структуру и инструменты для быстрой разработки веб-приложений.

Они различаются по уровню абстракции, функциональности и подходу к решению задач.

**Основные категории фреймворков:**

- **Full-stack фреймворки** — Django, Pyramid
- **Микрофреймворки** — Flask, FastAPI
- **Асинхронные фреймворки** — Tornado, Sanic, Quart
- **API-фреймворки** — FastAPI, Django REST Framework

## Django

### Описание:

**Django** — это высокоуровневый full-stack веб-фреймворк, который поощряет быструю разработку и чистый, прагматичный дизайн.

Он следует принципу `"Don't Repeat Yourself"` (`DRY`) и предоставляет множество встроенных функций.

### Установка и настройка:

```bash
# Установка Django
pip install django

# Создание нового проекта
django-admin startproject myproject

# Создание приложения
python manage.py startapp myapp

# Запуск сервера разработки
python manage.py runserver
```

### Базовая структура проекта:

```python
# settings.py - Основные настройки проекта
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Ваше приложение
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Модели и ORM:

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['available', 'created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    @property
    def is_in_stock(self):
        return self.stock > 0

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity

# Миграции
# python manage.py makemigrations
# python manage.py migrate
```

### Views и URL-маршруты:

```python
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category, Order, OrderItem
from .forms import ProductForm, OrderCreateForm
import json

# Function-based views
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Пагинация
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, 'shop/product/list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Получение похожих продуктов
    product_category = product.category
    similar_products = Product.objects.filter(
        category=product_category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'shop/product/detail.html', context)

@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

# Class-based views
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = None
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Похожие продукты
        product_category = self.object.category
        context['similar_products'] = Product.objects.filter(
            category=product_category,
            available=True
        ).exclude(id=self.object.id)[:4]
        return context

@staff_member_required
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product/form.html'
    success_url = reverse_lazy('product_list')

@staff_member_required
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product/form.html'
    success_url = reverse_lazy('product_list')

@staff_member_required
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product/confirm_delete.html'
    success_url = reverse_lazy('product_list')

# API views
def product_api_list(request):
    """API endpoint для получения списка продуктов"""
    products = Product.objects.filter(available=True)
    
    data = [{
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'category': product.category.name,
        'image': product.image.url if product.image else None,
        'in_stock': product.is_in_stock,
    } for product in products]
    
    return JsonResponse({'products': data})

# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('order/create/', views.create_order, name='order_create'),
    
    # Class-based views
    path('products/', views.ProductListView.as_view(), name='product_list_cbv'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail_cbv'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    # API endpoints
    path('api/products/', views.product_api_list, name='product_api_list'),
]
```

### Forms и валидация:
```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'category', 'image', 'stock', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        return stock

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):  # Пример валидации
            raise ValidationError("Please use company email address.")
        return email

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your Message',
        'rows': 5
    }))
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return message

# Использование форм в views
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка валидных данных
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Отправка email или другая логика
            # send_email(subject, message, email)
            
            return render(request, 'contact/success.html')
    else:
        form = ContactForm()
    
    return render(request, 'contact/form.html', {'form': form})
```

### Шаблоны и статические файлы:
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Shop{% endblock %}</title>
    {% load static %}
    <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'product_list' %}">My Shop</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'product_list' %}">Products</a>
                <a class="nav-link" href="#">Cart</a>
                {% if user.is_authenticated %}
                    <a class="nav-link" href="#">Profile</a>
                    <a class="nav-link" href="{% url 'admin:index' %}">Admin</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <footer class="bg-dark text-light text-center py-3 mt-5">
        <div class="container">
            <p>&copy; 2024 My Shop. All rights reserved.</p>
        </div>
    </footer>

    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

<!-- product/list.html -->
{% extends 'base.html' %}

{% block title %}Products{% if category %} in {{ category.name }}{% endif %}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-3">
        <h3>Categories</h3>
        <ul class="list-group">
            <li class="list-group-item {% if not category %}active{% endif %}">
                <a href="{% url 'product_list' %}" class="text-decoration-none">
                    All Products
                </a>
            </li>
            {% for cat in categories %}
                <li class="list-group-item {% if category == cat %}active{% endif %}">
                    <a href="{{ cat.get_absolute_url }}" class="text-decoration-none">
                        {{ cat.name }}
                    </a>
                </li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="col-md-9">
        <h1>{% if category %}{{ category.name }}{% else %}All Products{% endif %}</h1>
        
        <div class="row">
            {% for product in page_obj %}
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        {% if product.image %}
                            <img src="{{ product.image.url }}" class="card-img-top" alt="{{ product.name }}">
                        {% endif %}
                        <div class="card-body">
                            <h5 class="card-title">{{ product.name }}</h5>
                            <p class="card-text">{{ product.description|truncatewords:20 }}</p>
                            <p class="card-text"><strong>${{ product.price }}</strong></p>
                            <a href="{{ product.get_absolute_url }}" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <p>No products available.</p>
                </div>
            {% endfor %}
        </div>
        
        <!-- Пагинация -->
        {% if page_obj.has_other_pages %}
            <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                        </li>
                    {% endif %}
                    
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                            <li class="page-item active">
                                <span class="page-link">{{ num }}</span>
                            </li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                            </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
                        </li>
                    {% endif %}
                </ul>
            </nav>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Аутентификация и авторизация:
```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('product_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})

# Проверка прав доступа
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    # Только для сотрудников
    orders = Order.objects.all()[:10]
    return render(request, 'admin/dashboard.html', {'orders': orders})

# Class-based view с проверкой прав
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AdminProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = 'admin/product_list.html'
    context_object_name = 'products'

# signals.py - Автоматическое создание профиля пользователя
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# models.py - Расширение модели пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
```

## FastAPI

### Описание:
FastAPI — это современный, быстрый веб-фреймворк для создания API с использованием Python 3.7+ на основе стандартных аннотаций типов. Он обеспечивает автоматическую генерацию документации, встроенную валидацию данных и высокую производительность.

### Установка и настройка:
```bash
# Установка FastAPI и Uvicorn
pip install fastapi uvicorn[standard]

# Для дополнительных возможностей
pip install pydantic[email] python-multipart sqlalchemy databases[postgresql]
```

### Базовое приложение:
```python
# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

# Конфигурация безопасности
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Модели данных
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ProductBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Приложение
app = FastAPI(
    title="E-commerce API",
    description="API для интернет-магазина",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Безопасность
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Фейковая база данных (в реальном приложении использовать SQLAlchemy)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("adminpass"),
        "disabled": False,
    }
}

fake_products_db = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99, "category_id": 1, "created_at": datetime.now()},
    {"id": 2, "name": "Smartphone", "description": "Latest smartphone", "price": 699.99, "category_id": 1, "created_at": datetime.now()},
]

# Вспомогательные функции
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/products/", response_model=List[Product])
async def read_products(skip: int = 0, limit: int = 100):
    return fake_products_db[skip : skip + limit]

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    product = next((p for p in fake_products_db if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_active_user)):
    new_product = {
        "id": len(fake_products_db) + 1,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "created_at": datetime.now()
    }
    fake_products_db.append(new_product)
    return new_product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    product_update: ProductCreate,
    current_user: User = Depends(get_current_active_user)
):
    for i, product in enumerate(fake_products_db):
        if product["id"] == product_id:
            fake_products_db[i].update({
                "name": product_update.name,
                "description": product_update.description,
                "price": product_update.price,
                "category_id": product_update.category_id
            })
            return fake_products_db[i]
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    for i, product in enumerate(fake_products_db):
        if product["id"] == product_id:
            del fake_products_db[i]
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

# Middleware для логирования
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Обработка ошибок
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Расширенное приложение с SQLAlchemy:
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    address = Column(String)
    postal_code = Column(String)
    city = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    paid = Column(Boolean, default=False)
    status = Column(String, default="pending")
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    quantity = Column(Integer)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int = 0
    available: bool = True
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    price: float
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    postal_code: str
    city: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    paid: bool
    status: str
    items: List[OrderItem] = []
    
    class Config:
        orm_mode = True

# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: int = None):
    query = db.query(models.Product).filter(models.Product.available == True)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product_update.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# main.py (расширенная версия)
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced E-commerce API")

# Endpoints для пользователей
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoints для продуктов
@app.get("/products/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    category_id: int = None,
    db: Session = Depends(get_db)
):
    products = crud.get_products(db, skip=skip, limit=limit, category_id=category_id)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int, 
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db)
):
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = crud.delete_product(db, product_id=product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
```

## Flask

### Описание:
Flask — это легковесный WSGI веб-фреймворк. Он прост в использовании и легко расширяем, что делает его отличным выбором для небольших проектов и прототипирования.

### Установка и базовая настройка:
```bash
# Установка Flask
pip install flask

# Для дополнительных возможностей
pip install flask-sqlalchemy flask-login flask-wtf flask-mail
```

### Базовое приложение:
```python
# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Модели
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

# User loader для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# API endpoints
@app.route("/api/posts")
def api_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.isoformat(),
        'author': post.author.username
    } for post in posts])

@app.route("/api/posts/<int:post_id>")
def api_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.isoformat(),
        'author': post.author.username
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Blueprints для модульности
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    posts = Post.query.all()
    return render_template('admin/dashboard.html', users=users, posts=posts)

app.register_blueprint(admin_bp)

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### Шаблоны Jinja2:
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if title %}{{ title }} - Flask Blog{% else %}Flask Blog{% endif %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('home') }}">Flask Blog</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('home') }}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('about') }}">About</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('new_post') }}">New Post</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                                {{ current_user.username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{{ url_for('account') }}">Account</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{{ url_for('logout') }}">Logout</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('register') }}">Register</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

<!-- home.html -->
{% extends "base.html" %}

{% block content %}
    {% for post in posts.items %}
        <article class="media content-section">
            <div class="media-body">
                <div class="article-metadata">
                    <a class="mr-2" href="#">{{ post.author.username }}</a>
                    <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
                </div>
                <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
                <p class="article-content">{{ post.content[:100] }}...</p>
            </div>
        </article>
    {% endfor %}

    <!-- Пагинация -->
    {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
        {% if page_num %}
            {% if posts.page == page_num %}
                <a class="btn btn-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
            {% else %}
                <a class="btn btn-outline-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
            {% endif %}
        {% else %}
            ...
        {% endif %}
    {% endfor %}
{% endblock content %}
```

## Pyramid

### Описание:
Pyramid — это гибкий веб-фреймворк, который позволяет начинать с минимальной конфигурации и масштабироваться до сложных приложений.

### Установка и базовая настройка:
```bash
# Установка Pyramid
pip install pyramid pyramid_jinja2

# Создание проекта
pcreate -s alchemy myproject
cd myproject
pip install -e .
```

### Базовое приложение:
```python
# __init__.py
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config
from .models import DBSession, Base

def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    # Настройка сессии
    session_factory = SignedCookieSessionFactory('your-secret-session-key')
    
    config = Configurator(
        settings=settings,
        session_factory=session_factory
    )
    
    # Подключение Jinja2
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    
    # Маршруты
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    
    # Scan для views
    config.scan()
    
    return config.make_wsgi_app()

# models.py
from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer)

# views.py
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from .models import DBSession, User, Post
from .security import check_password

@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    posts = DBSession.query(Post).order_by(Post.created_at.desc()).limit(10).all()
    return {'posts': posts}

@view_config(route_name='about', renderer='templates/about.jinja2')
def about_view(request):
    return {}

@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = DBSession.query(User).filter_by(username=username).first()
        
        if user and check_password(password, user.password_hash):
            headers = remember(request, user.id)
            return HTTPFound(location='/', headers=headers)
        else:
            request.session.flash('Invalid username or password')
    
    return {}

@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)

# security.py
from passlib.hash import pbkdf2_sha256

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)
```

## Tornado

### Описание:
Tornado — это асинхронный веб-фреймворк и библиотека сетевых инструментов, разработанные для масштабируемых приложений реального времени.

### Установка и базовое приложение:
```bash
# Установка Tornado
pip install tornado

# Установка дополнительных зависимостей
pip install motor pymongo  # Для MongoDB
```

```python
# main.py
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from datetime import datetime
import asyncio

# WebSocket handler для реального времени
class ChatWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    
    def open(self):
        self.clients.add(self)
        print(f"WebSocket opened. Total clients: {len(self.clients)}")
        self.write_message(json.dumps({
            "type": "system",
            "message": "Connected to chat",
            "timestamp": datetime.now().isoformat()
        }))
    
    def on_message(self, message):
        try:
            data = json.loads(message)
            if data.get("type") == "chat":
                # Рассылка сообщения всем клиентам
                for client in self.clients:
                    if client != self:
                        client.write_message(json.dumps({
                            "type": "chat",
                            "username": data.get("username", "Anonymous"),
                            "message": data.get("message", ""),
                            "timestamp": datetime.now().isoformat()
                        }))
        except json.JSONDecodeError:
            self.write_message(json.dumps({
                "type": "error",
                "message": "Invalid JSON format"
            }))
    
    def on_close(self):
        self.clients.discard(self)
        print(f"WebSocket closed. Total clients: {len(self.clients)}")
    
    def check_origin(self, origin):
        # Разрешить подключения с любого origin (в продакшене ограничить)
        return True

# HTTP handlers
class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("index.html")

class ApiHandler(tornado.web.RequestHandler):
    async def get(self):
        # Асинхронная обработка API
        await asyncio.sleep(0.1)  # Имитация асинхронной операции
        data = {
            "message": "Hello from Tornado API",
            "timestamp": datetime.now().isoformat(),
            "clients_online": len(ChatWebSocket.clients)
        }
        self.write(json.dumps(data))
    
    async def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            response = {
                "received": data,
                "timestamp": datetime.now().isoformat()
            }
            self.write(json.dumps(response))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write(json.dumps({"error": "Invalid JSON"}))

# Async database operations (пример с Motor для MongoDB)
import motor.motor_tornado

class DatabaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.settings['db']
    
    async def get(self):
        # Асинхронный запрос к базе данных
        cursor = self.db.users.find({}, {'_id': 0})
        users = await cursor.to_list(length=100)
        self.write(json.dumps(users))
    
    async def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            result = await self.db.users.insert_one(data)
            self.write(json.dumps({
                "inserted_id": str(result.inserted_id),
                "timestamp": datetime.now().isoformat()
            }))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

# Application setup
def make_app():
    # Подключение к MongoDB
    client = motor.motor_tornado.MotorClient('mongodb://localhost:27017')
    db = client.chat_database
    
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api", ApiHandler),
        (r"/api/users", DatabaseHandler, dict(db=db)),
        (r"/websocket", ChatWebSocket),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], 
    template_path="templates",
    static_path="static",
    debug=True,
    db=db  # Передача db в handlers
    )

# Templates
# templates/index.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>Tornado Chat</title>
    <script src="/static/chat.js"></script>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="username" placeholder="Your name">
            <input type="text" id="message" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
</body>
</html>
"""

# static/chat.js
"""
let ws;

window.onload = function() {
    ws = new WebSocket("ws://" + window.location.host + "/websocket");
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        displayMessage(data);
    };
    
    ws.onclose = function() {
        console.log("Connection closed");
    };
};

function sendMessage() {
    const username = document.getElementById('username').value || 'Anonymous';
    const message = document.getElementById('message').value;
    
    if (message.trim()) {
        ws.send(JSON.stringify({
            type: 'chat',
            username: username,
            message: message
        }));
        
        document.getElementById('message').value = '';
    }
}

function displayMessage(data) {
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    
    if (data.type === 'system') {
        messageElement.innerHTML = `<em>${data.message}</em>`;
    } else {
        messageElement.innerHTML = `
            <strong>${data.username}:</strong> 
            ${data.message}
            <span class="timestamp">${new Date(data.timestamp).toLocaleTimeString()}</span>
        `;
    }
    
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight;
}
"""

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
```

## Sanic

### Описание:
Sanic — это асинхронный веб-сервер и фреймворк, написанный на Python 3.7+, который разработан для скорости.

### Установка и базовое приложение:
```bash
# Установка Sanic
pip install sanic

# Для дополнительных возможностей
pip install sanic-ext sanic-jwt databases[postgresql] asyncpg
```

```python
# app.py
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json, text, html
from sanic.exceptions import NotFound, ServerError
from sanic.websocket import WebSocketConnection
import asyncio
import json as json_module
from datetime import datetime

app = Sanic("AsyncWebApp")

# Middleware
@app.middleware("request")
async def add_timestamp(request):
    request.ctx.start_time = datetime.now()

@app.middleware("response")
async def add_process_time(request, response):
    process_time = datetime.now() - request.ctx.start_time
    response.headers["X-Process-Time"] = str(process_time.total_seconds())

# Static files
app.static('/static', './static')

# Routes
@app.route("/")
async def index(request: Request):
    return html("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sanic App</title>
        <script src="/static/main.js"></script>
    </head>
    <body>
        <h1>Welcome to Sanic!</h1>
        <div id="content"></div>
    </body>
    </html>
    """)

@app.route("/api/data")
async def api_data(request: Request):
    # Асинхронная операция
    await asyncio.sleep(0.1)
    return json({
        "message": "Hello from Sanic API",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/users/<user_id:int>")
async def get_user(request: Request, user_id: int):
    # Имитация получения пользователя из базы данных
    user_data = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }
    return json(user_data)

# WebSocket endpoint
@app.websocket("/websocket")
async def websocket_endpoint(request: Request, ws: WebSocketConnection):
    while True:
        try:
            data = await ws.recv()
            message = json_module.loads(data)
            
            # Echo сообщение обратно всем клиентам
            response_data = {
                "type": "echo",
                "message": message.get("message", ""),
                "timestamp": datetime.now().isoformat()
            }
            
            await ws.send(json_module.dumps(response_data))
            
        except Exception as e:
            print(f"WebSocket error: {e}")
            break

# Background tasks
async def background_task():
    while True:
        print("Background task running...")
        await asyncio.sleep(10)

@app.before_server_start
async def start_background_task(app, loop):
    app.add_task(background_task())

# Error handlers
@app.exception(NotFound)
async def ignore_404s(request, exception):
    return text("Oops, that page doesn't exist!", status=404)

@app.exception(ServerError)
async def handle_server_error(request, exception):
    return json({"error": "Internal server error"}, status=500)

# Blueprints для модульности
from sanic.blueprints import Blueprint

api_bp = Blueprint('api', url_prefix='/api/v1')

@api_bp.get('/health')
async def health_check(request):
    return json({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@api_bp.post('/process')
async def process_data(request):
    data = request.json
    # Асинхронная обработка данных
    result = await asyncio.sleep(1)  # Имитация обработки
    return json({"result": "processed", "data": data})

app.blueprint(api_bp)

# Middleware с классами
class AuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request):
        # Простая проверка токена
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return response.json({"error": "Unauthorized"}, status=401)
        
        token = auth_header.split(' ')[1]
        if token != "secret-token":
            return response.json({"error": "Invalid token"}, status=401)

# Применение middleware
# app.register_middleware(AuthMiddleware(app), "request")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
```

## Quart

### Описание:
Quart — это асинхронная версия Flask, которая предоставляет те же возможности, но с поддержкой async/await.

### Установка и базовое приложение:
```bash
# Установка Quart
pip install quart

# Для дополнительных возможностей
pip install quart-cors quart-session databases[postgresql] asyncpg
```

```python
# app.py
from quart import Quart, request, jsonify, render_template, websocket
import asyncio
import json
from datetime import datetime

app = Quart(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['DEBUG'] = True

# Middleware
@app.before_request
async def before_request():
    request.start_time = datetime.now()

@app.after_request
async def after_request(response):
    process_time = datetime.now() - request.start_time
    response.headers['X-Process-Time'] = str(process_time.total_seconds())
    return response

# Routes
@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/api/data')
async def api_data():
    # Асинхронная операция
    await asyncio.sleep(0.1)
    return jsonify({
        'message': 'Hello from Quart API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/users/<int:user_id>')
async def get_user(user_id):
    user_data = {
        'id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com'
    }
    return jsonify(user_data)

# WebSocket endpoint
@app.websocket('/ws')
async def ws():
    while True:
        try:
            data = await websocket.receive()
            message = json.loads(data)
            
            response = {
                'type': 'echo',
                'message': message.get('message', ''),
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(response))
        except Exception as e:
            print(f'WebSocket error: {e}')
            break

# Background tasks
async def background_task():
    while True:
        print('Background task running...')
        await asyncio.sleep(10)

@app.before_serving
async def startup():
    app.background_task = asyncio.ensure_future(background_task())

@app.after_serving
async def cleanup():
    app.background_task.cancel()

# Error handlers
@app.errorhandler(404)
async def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## Практические примеры

### Пример 1: REST API для блога
```python
# blog_api.py (FastAPI)
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Blog API", version="1.0.0")

# Модели данных
class PostBase(BaseModel):
    title: str
    content: str
    author: str
    tags: List[str] = []

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Фейковая база данных
posts_db = []
counter = 1

# Вспомогательные функции
def get_post_by_id(post_id: int) -> Optional[dict]:
    return next((post for post in posts_db if post["id"] == post_id), None)

def create_post(post_data: PostCreate) -> dict:
    global counter
    post = {
        "id": counter,
        "title": post_data.title,
        "content": post_data.content,
        "author": post_data.author,
        "tags": post_data.tags,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    posts_db.append(post)
    counter += 1
    return post

# Endpoints
@app.get("/posts", response_model=List[Post])
async def get_posts(skip: int = 0, limit: int = 10, tag: Optional[str] = None):
    posts = posts_db
    if tag:
        posts = [post for post in posts if tag in post["tags"]]
    return posts[skip:skip + limit]

@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=Post)
async def create_post(post: PostCreate):
    return create_post(post)

@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostCreate):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.update({
        "title": post_update.title,
        "content": post_update.content,
        "author": post_update.author,
        "tags": post_update.tags,
        "updated_at": datetime.now()
    })
    return post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    posts_db.remove(post)
    return {"message": "Post deleted successfully"}

# Заполнение тестовыми данными
@app.on_event("startup")
async def startup_event():
    create_post(PostCreate(
        title="Getting Started with Python",
        content="Python is a versatile programming language...",
        author="John Doe",
        tags=["python", "tutorial"]
    ))
    create_post(PostCreate(
        title="Web Development with Django",
        content="Django is a high-level Python web framework...",
        author="Jane Smith",
        tags=["django", "web", "python"]
    ))
```

### Пример 2: Асинхронный чат с WebSocket
```python
# chat_app.py (Sanic)
from sanic import Sanic, response
from sanic.websocket import WebSocketConnection
import json
from datetime import datetime
from typing import Set

app = Sanic("AsyncChat")

# Хранение активных соединений
connected_clients: Set[WebSocketConnection] = set()

@app.route("/")
async def index(request):
    return response.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Async Chat</title>
        <style>
            #chat { height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; }
            #input { display: flex; margin-top: 10px; }
            #message { flex: 1; padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h1>Async Chat Room</h1>
        <div id="chat"></div>
        <div id="input">
            <input type="text" id="username" placeholder="Your name" value="Anonymous">
            <input type="text" id="message" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <script>
            const ws = new WebSocket('ws://' + window.location.host + '/websocket');
            const chat = document.getElementById('chat');
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
                chat.appendChild(messageDiv);
                chat.scrollTop = chat.scrollHeight;
            };
            
            function sendMessage() {
                const username = document.getElementById('username').value;
                const message = document.getElementById('message').value;
                
                if (message.trim()) {
                    ws.send(JSON.stringify({
                        username: username,
                        message: message,
                        timestamp: new Date().toISOString()
                    }));
                    document.getElementById('message').value = '';
                }
            }
            
            document.getElementById('message').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """)

@app.websocket('/websocket')
async def websocket_handler(request, ws):
    connected_clients.add(ws)
    
    try:
        # Отправка приветственного сообщения
        await ws.send(json.dumps({
            'username': 'System',
            'message': 'Welcome to the chat room!'
        }))
        
        while True:
            data = await ws.recv()
            message_data = json.loads(data)
            
            # Рассылка сообщения всем клиентам
            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send(json.dumps(message_data))
                except:
                    disconnected.add(client)
            
            # Удаление отключившихся клиентов
            connected_clients.difference_update(disconnected)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.discard(ws)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```

### Пример 3: Микросервис с Docker
```python
# user_service.py (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import databases
import sqlalchemy
from datetime import datetime

# Конфигурация базы данных
DATABASE_URL = "postgresql://user:password@db:5432/users_db"
database = databases.Database(DATABASE_URL)

# Модели SQLAlchemy
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

# Pydantic модели
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Приложение
app = FastAPI(title="User Service", version="1.0.0")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    query = users.insert().values(
        username=user.username,
        email=user.email,
        created_at=datetime.utcnow()
    )
    last_record_id = await database.execute(query)
    
    # Получение созданного пользователя
    query = users.select().where(users.c.id == last_record_id)
    return await database.fetch_one(query)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
```

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "user_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  user-service:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/users_db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: users_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Сравнение фреймворков

### Матрица сравнения:

| Фреймворк | Тип | Производительность | Простота | Масштабируемость | Сообщество |
|-----------|-----|-------------------|----------|------------------|------------|
| **Django** | Full-stack | Высокая | Высокая | Высокая | Очень большое |
| **FastAPI** | API | Очень высокая | Высокая | Высокая | Быстро растущее |
| **Flask** | Микро | Средняя | Очень высокая | Средняя | Большое |
| **Pyramid** | Гибкий | Высокая | Средняя | Высокая | Среднее |
| **Tornado** | Асинхронный | Очень высокая | Средняя | Высокая | Среднее |
| **Sanic** | Асинхронный | Очень высокая | Высокая | Высокая | Растущее |
| **Quart** | Асинхронный Flask | Очень высокая | Очень высокая | Высокая | Растущее |

### Когда использовать каждый фреймворк:

```python
# Матрица выбора фреймворка
FRAMEWORK_SELECTION = {
    'simple_api': ['FastAPI', 'Flask'],
    'complex_web_app': ['Django', 'Pyramid'],
    'real_time_app': ['Tornado', 'Sanic', 'Quart'],
    'microservices': ['FastAPI', 'Flask', 'Sanic'],
    'rapid_prototyping': ['Flask', 'FastAPI'],
    'enterprise_app': ['Django', 'Pyramid'],
    'high_performance': ['FastAPI', 'Tornado', 'Sanic'],
    'beginner_friendly': ['Flask', 'Django']
}

def select_framework(project_requirements):
    """Выбор подходящего фреймворка"""
    scores = {}
    
    for framework_type, suitable_projects in FRAMEWORK_SELECTION.items():
        score = 0
        for requirement in project_requirements:
            if requirement in suitable_projects:
                score += 1
        scores[framework_type] = score
    
    return max(scores.items(), key=lambda x: x[1])[0]

# Пример использования
requirements = ['simple_api', 'high_performance', 'beginner_friendly']
recommended_framework = select_framework(requirements)
print(f"Рекомендуемый фреймворк: {recommended_framework}")
```

## Лучшие практики

### 1. Структура проекта:
```python
# Рекомендуемая структура для крупных проектов
project_structure = {
    'myproject/': {
        'app/': {
            '__init__.py': 'Инициализация приложения',
            'models/': {
                '__init__.py': '',
                'user.py': 'Модели пользователей',
                'product.py': 'Модели продуктов'
            },
            'views/': {
                '__init__.py': '',
                'user_views.py': 'Views для пользователей',
                'product_views.py': 'Views для продуктов'
            },
            'api/': {
                '__init__.py': '',
                'v1/': {
                    '__init__.py': '',
                    'user_api.py': 'API v1 для пользователей',
                    'product_api.py': 'API v1 для продуктов'
                }
            },
            'utils/': {
                '__init__.py': '',
                'helpers.py': 'Вспомогательные функции',
                'validators.py': 'Валидаторы'
            },
            'tests/': {
                '__init__.py': '',
                'test_models.py': 'Тесты моделей',
                'test_views.py': 'Тесты views',
                'test_api.py': 'Тесты API'
            }
        },
        'config/': {
            '__init__.py': '',
            'settings.py': 'Основные настройки',
            'database.py': 'Настройки базы данных',
            'logging.py': 'Настройки логирования'
        },
        'migrations/': 'Миграции базы данных',
        'static/': 'Статические файлы',
        'templates/': 'Шаблоны',
        'requirements.txt': 'Зависимости',
        'README.md': 'Документация',
        'manage.py': 'Управляющий скрипт (Django)',
        'main.py': 'Точка входа'
    }
}
```

### 2. Обработка ошибок:
```python
# error_handlers.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

def setup_error_handlers(app: FastAPI):
    @app.exception_handler(CustomHTTPException)
    async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
        logger.error(f"Custom error {exc.error_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail
                }
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": exc.errors()
                }
            }
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Exception):
        logger.error(f"Internal server error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal server error occurred"
                }
            }
        )

# Использование в приложении
app = FastAPI()
setup_error_handlers(app)

@app.get("/test-error")
async def test_error():
    raise CustomHTTPException(
        status_code=400,
        detail="This is a test error",
        error_code="TEST_ERROR"
    )
```

### 3. Логирование и мониторинг:
```python
# logging_config.py
import logging
import logging.config
from datetime import datetime

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
        'json': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
        },
        'error_file': {
            'level': 'ERROR',
            'formatter': 'detailed',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'database': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

def setup_logging():
    """Настройка логирования"""
    import os
    
    # Создание директории для логов
    os.makedirs('logs', exist_ok=True)
    
    # Применение конфигурации
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Тестовые сообщения
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")
    logger.debug("Debug mode enabled")

# middleware.py
class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger('app.request')
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = datetime.now()
        
        # Логирование запроса
        self.logger.info(f"{scope['method']} {scope['path']} - Started")
        
        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                process_time = datetime.now() - start_time
                self.logger.info(
                    f"{scope['method']} {scope['path']} - "
                    f"{message['status']} - {process_time.total_seconds():.3f}s"
                )
            await send(message)
        
        await self.app(scope, receive, wrapped_send)

# Использование
# setup_logging()
# app.add_middleware(RequestLoggingMiddleware)
```

### 4. Безопасность:
```python
# security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import secrets

# Настройки безопасности
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

# rate_limiting.py
from collections import defaultdict
class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = datetime.now().timestamp()
        
        # Удаление старых записей
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Проверка лимита
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Добавление текущего запроса
        self.requests[client_id].append(now)
        return True

# input_validation.py
from pydantic import BaseModel, validator, EmailStr
import re

class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

# Использование валидации
try:
    user_data = UserRegistration(
        username="testuser",
        email="test@example.com",
        password="SecurePass123"
    )
    print("Valid user data:", user_data.dict())
except ValueError as e:
    print("Validation error:", e)
```

### 5. Тестирование:
```python
# test_example.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# conftest.py
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

@pytest.fixture
def client():
    from main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_db():
    with patch('app.database.get_db') as mock_get_db:
        mock_session = Mock()
        mock_get_db.return_value = mock_session
        yield mock_session

# test_api.py
class TestUserAPI:
    def test_create_user_success(self, client, mock_db):
        # Настройка мока
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Вызов API
        response = client.post("/users/", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        })
        
        # Проверки
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        
        # Проверка вызовов
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_create_user_duplicate_email(self, client, mock_db):
        # Настройка мока для дубликата
        mock_db.query().filter().first.return_value = Mock()
        
        response = client.post("/users/", json={
            "username": "testuser",
            "email": "existing@example.com",
            "password": "securepassword123"
        })
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_get_user_not_found(self, client, mock_db):
        # Настройка мока для несуществующего пользователя
        mock_db.query().get.return_value = None
        
        response = client.get("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

# test_models.py
class TestUserModel:
    def test_password_hashing(self):
        from app.models import User
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("mypassword")
        
        assert user.check_password("mypassword") is True
        assert user.check_password("wrongpassword") is False
        
    def test_repr(self):
        from app.models import User
        
        user = User(username="testuser", email="test@example.com")
        assert repr(user) == "User('testuser', 'test@example.com')"

# test_security.py
class TestSecurity:
    def test_password_hashing(self):
        from app.security import SecurityManager
        
        password = "testpassword123"
        hashed = SecurityManager.get_password_hash(password)
        
        assert hashed != password
        assert SecurityManager.verify_password(password, hashed) is True
        assert SecurityManager.verify_password("wrongpassword", hashed) is False
    
    def test_jwt_token(self):
        from app.security import SecurityManager
        from datetime import timedelta
        
        data = {"sub": "testuser"}
        token = SecurityManager.create_access_token(data, timedelta(minutes=30))
        
        payload = SecurityManager.verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert "exp" in payload
```

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/обучение-технологиям-и-языкам-программирования)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.