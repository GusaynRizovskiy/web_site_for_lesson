from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages  # Используется для уведомлений
from django.http import HttpResponseRedirect  # Используется для явной обработки ошибок

from .models import Product, CartItem, Order


# Форма регистрации
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# Список продуктов (Главная страница)
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


# CRUD для продуктов (только для админа)
@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']  # Используем 'image'
    success_url = reverse_lazy('product_list')
    template_name = 'product_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('product_list')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']  # Используем 'image'
    success_url = reverse_lazy('product_list')
    template_name = 'product_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('product_list')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'product_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('product_list')
        return super().dispatch(request, *args, **kwargs)


# Добавление продукта в корзину
@login_required
def add_to_cart(request, product_id):
    # ПЕРВАЯ ПРОВЕРКА: Если @login_required не сработал или сессия нарушена
    if not request.user.is_authenticated:
        messages.error(request, "Пожалуйста, войдите, чтобы добавить товар в корзину.")
        return redirect('login')

    try:
        product = get_object_or_404(Product, id=product_id)

        # Логика добавления/обновления
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Сообщение об успешном добавлении (используется в base.html)
        messages.success(request, f'"{product.name}" добавлен в корзину!')

        # ИЗМЕНЕНИЕ: Возвращаем пользователя на список продуктов
        return redirect('product_list')

    except Exception as e:
        # ОБРАБОТКА ОШИБКИ: Гарантируем возврат HttpResponse, устраняя ошибку ValueError
        messages.error(request, f"Не удалось добавить товар в корзину. Ошибка: {e}")
        return redirect('product_list')  # Возвращаем на список даже при ошибке


# Просмотр корзины
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Удаление из корзины (или уменьшение количества)
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# Оформление заказа
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Ваша корзина пуста.")
        return redirect('product_list')

    total_amount = sum(item.total_price() for item in cart_items)

    # 1. Создаем Заказ
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        is_paid=True
    )

    # 2. Очищаем корзину
    cart_items.delete()

    messages.success(request, f"Заказ №{order.id} успешно оформлен! Общая сумма: {order.total_amount} руб.")

    return render(request, 'checkout.html', {'order': order})