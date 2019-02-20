from django.conf import settings
from rest_framework import serializers

from products.models import Product, GiftCard


class GetPriceSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=10)
    gift_card_code = serializers.CharField(required=False, allow_blank=True, max_length=10)
    date = serializers.DateField(input_formats=[settings.API['DATE_FORMAT']])

    def validate(self, data):
        product_code = data.get('product_code')
        gift_card_code = data.get('gift_card_code')
        date = data.get('date')

        try:
            data['product'] = Product.objects.get(code=product_code)
        except Product.DoesNotExist:
            raise serializers.ValidationError('There is no Product with {0} code.'.format(product_code))

        if gift_card_code:
            try:
                data['gift_card'] = GiftCard.objects.date_in(date).get(code=gift_card_code)
            except GiftCard.DoesNotExist:
                raise serializers.ValidationError('There is no Gift Card with {0} code on {1}.'.format(
                    product_code,
                    date
                ))
        else:
            data['gift_card'] = None

        return data
