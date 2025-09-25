from django.urls import path
from . import views
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, SignUpView

urlpatterns = [
    # Главная страница (Список продуктов)
    path('', ProductListView.as_view(), name='product_list'),

    # Аутентификация
    path('signup/', SignUpView.as_view(), name='signup'),

    # CRUD для продуктов (Админ)
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Корзина
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Оформление заказа
    path('checkout/', views.checkout, name='checkout'),
]