from django.contrib import admin
from django.urls import path, include
# Импортируем для обработки медиафайлов в режиме разработки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('grocery.urls')),
]

# Важно: Эта настройка нужна ТОЛЬКО для режима разработки (Debug=True).
# В продакшене медиафайлы должен отдавать веб-сервер (Nginx, Apache).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)