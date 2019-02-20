from django.db import models
from django.db.models import Q

from products.tools import format_price


class DateQuerySet(models.QuerySet):
    def date_in(self, date):
        return self.filter(
            Q(date_start__lte=date),
            Q(date_end__gte=date) | Q(date_end__isnull=True),
        )


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.code)

    @property
    def formatted_price(self):
        return format_price(self.price)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    objects = DateQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return format_price(self.amount)


class ProductPrice(models.Model):
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_prices')
    objects = DateQuerySet.as_manager()

    class Meta:
        db_table = 'product_price'

    def __str__(self):
        return '{} - {} from {} to {}'.format(self.product, self.price, self.date_start, self.date_end or '∞')

    @property
    def formatted_price(self):
        return format_price(self.price)
