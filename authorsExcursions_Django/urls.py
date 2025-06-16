from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('authorsExcursions.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
]
