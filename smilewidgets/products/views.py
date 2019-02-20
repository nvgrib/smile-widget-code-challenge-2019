from rest_framework.views import APIView
from rest_framework.response import Response
from djangorestframework_camel_case.util import underscoreize

from products.serializers import GetPriceSerializer
from products.tools import format_price


class ProductPriceItemView(APIView):
    def get(self, request):
        get_price_serializer = GetPriceSerializer(data=underscoreize(request.query_params))
        get_price_serializer.is_valid(raise_exception=True)

        date = get_price_serializer.validated_data['date']
        gift_card = get_price_serializer.validated_data['gift_card']
        product = get_price_serializer.validated_data['product']
        product_price = product.product_prices.date_in(date).order_by('price').first()

        final_price = product.price

        if product_price:
            final_price = product_price.price

        if gift_card:
            final_price -= gift_card.amount
            final_price = 0 if final_price < 0 else final_price

        return Response({'productPrice': format_price(final_price)})
