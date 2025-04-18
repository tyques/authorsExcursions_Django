from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class RegisteredUser(User):
    def view_personal_account(self):
        """Просмотр личного кабинета"""
        pass

    def edit_profile(self):
        """Редактирование профиля"""
        pass

    def view_visited_tours(self):
        """Просмотр посещенных туров"""
        from .models import Tour
        return Tour.objects.filter(participants=self)

    class Meta:
        verbose_name = 'Registered User'
        verbose_name_plural = 'Registered Users'


class Guide(RegisteredUser):
    def add_tour(self, tour_data):
        """Добавление нового тура"""
        from .models import Tour
        return Tour.objects.create(guide=self, **tour_data)

    def edit_tour(self, tour_id, new_data):
        """Редактирование тура"""
        from .models import Tour
        tour = Tour.objects.get(pk=tour_id, guide=self)
        for key, value in new_data.items():
            setattr(tour, key, value)
        tour.save()
        return tour

    def answer_question(self, question, answer):
        """Ответ на вопрос"""
        question.answer = answer
        question.save()
        return question

    class Meta:
        verbose_name = 'Guide'
        verbose_name_plural = 'Guides'


class Administrator(RegisteredUser):
    def manage_catalog(self):
        """Управление каталогом"""
        pass

    def delete_review(self, review):
        """Удаление отзыва"""
        review.delete()

    def delete_tour(self, tour):
        """Удаление тура"""
        tour.delete()

    def delete_question(self, question):
        """Удаление вопроса"""
        question.delete()

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'


class Tour(models.Model):
    excID = models.AutoField(primary_key=True)
    excName = models.CharField(max_length=200)
    excCountry = models.CharField(max_length=100)
    excCity = models.CharField(max_length=100)
    excDate = models.DateTimeField()
    peopleNumberCurrent = models.IntegerField(default=0)
    childPresence = models.BooleanField(default=False)
    ageRestrict = models.IntegerField(default=0)
    pathDiff = models.CharField(max_length=50, blank=True)
    excDesc = models.TextField()
    excPrice = models.FloatField()
    excScore = models.FloatField(default=0.0)
    excStatus = models.SmallIntegerField(default=1)  # 0 - неактивен, 1 - активен

    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='tours')
    participants = models.ManyToManyField(RegisteredUser, related_name='visited_tours', blank=True)

    def __str__(self):
        return f"{self.excName} ({self.excCity}, {self.excCountry})"

    class Meta:
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'


class Catalog(models.Model):
    tours = models.ManyToManyField(Tour, related_name='catalogs')

    def filter_by_tags(self, tags):
        """Фильтрация туров по тегам"""
        return self.tours.filter(tags__icontains=tags)

    def __str__(self):
        return f"Catalog with {self.tours.count()} tours"

    class Meta:
        verbose_name = 'Catalog'
        verbose_name_plural = 'Catalogs'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    score = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.tour.excName}"

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Tour, through='CartItem')

    def add_tour(self, tour):
        """Добавление тура в корзину"""
        CartItem.objects.get_or_create(cart=self, tour=tour)

    def remove_tour(self, tour_id):
        """Удаление тура из корзины"""
        CartItem.objects.filter(cart=self, tour_id=tour_id).delete()

    def clear(self):
        """Очистка корзины"""
        self.items.clear()

    def get_amount(self):
        """Получение общей суммы"""
        return sum(item.tour.excPrice for item in self.cart_items.all())

    def create_order(self):
        """Создание заказа из корзины"""
        order = Order.objects.create(customer=self.user, cost=self.get_amount())
        for item in self.cart_items.all():
            order.tours.add(item.tour)
        self.clear()
        return order

    def __str__(self):
        return f"Cart of {self.user.username}"

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'tour')


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    customer = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    tours = models.ManyToManyField(Tour)
    cost = models.FloatField()
    promocode = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    PAYMENT_METHODS = [
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        ('BT', 'Bank Transfer'),
    ]
    paymentMethod = models.CharField(max_length=2, choices=PAYMENT_METHODS, blank=True)

    def choose_payment(self, method):
        """Выбор способа оплаты"""
        self.paymentMethod = method
        self.save()

    @classmethod
    def get_order(cls, order_id):
        """Получение заказа по ID"""
        return cls.objects.get(pk=order_id)

    def __str__(self):
        return f"Order #{self.orderId} by {self.customer.username}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
