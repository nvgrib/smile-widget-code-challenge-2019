from django.urls import path

from products.views import ProductPriceItemView


urlpatterns = [
    path('get-price/', ProductPriceItemView.as_view())
]