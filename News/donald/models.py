from django.db import models
from datetime import datetime
from datetime import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    category = models.CharField(max_length=20)


# cap_big = Product.objects.create(name="Монитор", price=9999.0)


# cap = Product(name='Monitor', price=9999.0)
# cap.save()


director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Director'),
    (admin, 'Admin'),
    (cook, 'Cook'),
    (cashier, 'Cashier'),
    (cleaner, 'Cleaner')
]


class Staff(models.Model):
    full_name: str = models.CharField(max_length=255)
    position: str = models.CharField(max_length=2, choices=POSITIONS, default='Cashier')
    labor_contract: int = models.IntegerField(default=0)

    def get_last_name(self):
        return self.full_name.split()[0]


class Orders(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.99)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    _amount: int = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True)
    email = models.CharField(max_length=255, blank=True)
