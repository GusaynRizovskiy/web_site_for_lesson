from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Включаем встроенные маршруты аутентификации (login, logout)
    path('accounts/', include('django.contrib.auth.urls')),
    # Все остальные маршруты идут в наше приложение 'grocery'
    path('', include('grocery.urls')),
]