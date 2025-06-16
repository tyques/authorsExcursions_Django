from decimal import Decimal
from django.conf import settings
from authorsExcursions.models import Tour # Используем вашу модель Tour

class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, tour, quantity=1, update_quantity=False):
        """
        Добавить тур в корзину или обновить его количество.
        """
        tour_id = str(tour.excID)
        if tour_id not in self.cart:
            self.cart[tour_id] = {'quantity': 0,
                                     'price': str(tour.excPrice)}
        if update_quantity:
            self.cart[tour_id]['quantity'] = quantity
        else:
            self.cart[tour_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, tour):
        """
        Удаление тура из корзины.
        """
        tour_id = str(tour.excID)
        if tour_id in self.cart:
            del self.cart[tour_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение туров из базы данных.
        """
        tour_ids = self.cart.keys()
        # получение объектов Tour и добавление их в корзину
        tours = Tour.objects.filter(excID__in=tour_ids)

        cart = self.cart.copy()
        for tour in tours:
            cart[str(tour.excID)]['tour'] = tour

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True