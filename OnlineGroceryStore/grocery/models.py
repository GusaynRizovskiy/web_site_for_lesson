from django.db import models
from django.contrib.auth.models import User

# Модель Продукта
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # ИЗМЕНЕНИЕ ЗДЕСЬ: используем ImageField
    # 'product_images/' - это подпапка внутри MEDIA_ROOT, где будут храниться изображения
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.name

    # Вспомогательный метод, чтобы получать полный URL изображения
    def get_image_url(self):
        # Если изображение загружено, возвращаем его URL, иначе - ссылку на заглушку
        if self.image:
            return self.image.url
        return 'https://via.placeholder.com/400x200?text=Нет+изображения'

# Модель Элемента Корзины
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.IntegerField(default=1, verbose_name="Количество")

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.user.username}"

# Модель Заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"