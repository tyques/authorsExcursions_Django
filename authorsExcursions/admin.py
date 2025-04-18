from django.contrib import admin

from authorsExcursions.models import User, RegisteredUser, Guide, Administrator, Tour, Cart, CartItem, Order

# Register your models here.

admin.site.register(User)
admin.site.register(RegisteredUser)
admin.site.register(Guide)
admin.site.register(Administrator)
admin.site.register(Tour)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)

# каталог, фидбек
