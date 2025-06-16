# ==================== C:\Users\user\PycharmProjects\authorsExcursions_Django\cart\urls.py ====================
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:tour_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:tour_id>/', views.cart_remove, name='cart_remove'),
]