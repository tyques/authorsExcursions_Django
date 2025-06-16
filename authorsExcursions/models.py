from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Определяем роли, которые могут быть у пользователя
    ROLE_CHOICES = (
        ('registered', 'Registered User'),
        ('guide', 'Guide'),
        ('administrator', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='registered')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

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
    excStatus = models.SmallIntegerField(default=1)

    guide = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tours',
        limit_choices_to={'profile__role': 'guide'}
    )
    # Здесь тоже ссылаемся на встроенного пользователя
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='visited_tours',
        blank=True
    )

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    # Модель уже использует правильную связь, это хорошо
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Tour, through='CartItem')

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.tour.excPrice * self.quantity

