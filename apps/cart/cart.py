from decimal import Decimal

from django.conf import settings

from apps.product.models import CartItem, CartModel, Product


class Cart:
    def __init__(self, request, user=None):
        """
        Инициализируем корзину
        """
        self.session = request.session
        self.user = user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            if item['product'].discount:
                item['price'] -= item['price'] * item['product'].discount / 100
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            price = product.price
            if product.discount:
                price -= price * product.discount / 100
            self.cart[product_id] = {'quantity': 0, 'price': str(price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.user:
            cart_instance, created = CartModel.objects.get_or_create(user=self.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart_instance, product=product)
            if update_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

        if self.user:
            cart_instance, created = CartModel.objects.get_or_create(user=self.user)
            cart_item = CartItem.objects.filter(cart=cart_instance, product=product).first()
            if cart_item:
                cart_item.delete()

        self.save()

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
