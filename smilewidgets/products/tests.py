from django.test import TestCase
from django.conf import settings
from datetime import datetime

from products.tools import format_price


class ApiTestCase(TestCase):
    fixtures = ['0001_fixtures.json', '0002_fixtures.json' ]

    url = '/api/get-price/'

    big_widget = 'big_widget'
    sm_widget = 'sm_widget'
    gift_card = '10OFF'

    year2018 = datetime(2018, 7, 2).strftime(settings.API['DATE_FORMAT'])
    blackFriday2018 = datetime(2018, 11, 24).strftime(settings.API['DATE_FORMAT'])
    year2019 = datetime(2019, 1, 1).strftime(settings.API['DATE_FORMAT'])

    def test_2018_big_widget(self):
        resp = self.client.get(self.url, data={
            'date': datetime(2018, 7, 2).strftime(settings.API['DATE_FORMAT']),
            'productCode': self.big_widget
        })

        self.assertEqual(resp.data['productPrice'], format_price(100000))

    def test_2018_sm_widget(self):
        resp = self.client.get(self.url, data={
            'date': datetime(2018, 7, 2).strftime(settings.API['DATE_FORMAT']),
            'productCode': self.sm_widget
        })

        self.assertEqual(resp.data['productPrice'], format_price(9900))

    def test_blackFriday2018_big_widget(self):
        resp = self.client.get(self.url, data={
            'date': self.blackFriday2018,
            'productCode': self.big_widget,
        })

        self.assertEqual(resp.data['productPrice'], format_price(80000))

    def test_blackFriday2018_sm_widget(self):
        resp = self.client.get(self.url, data={
            'date': self.blackFriday2018,
            'productCode': self.sm_widget
        })

        self.assertEqual(resp.data['productPrice'], format_price(0))

    def test_2019_big_widget(self):
        resp = self.client.get(self.url, data={
            'date': self.year2019,
            'productCode': self.big_widget
        })

        self.assertEqual(resp.data['productPrice'], format_price(120000))

    def test_2019_sm_widget(self):
        resp = self.client.get(self.url, data={
            'date': self.year2019,
            'productCode': self.sm_widget
        })

        self.assertEqual(resp.data['productPrice'], format_price(12500))

    def test_2018_big_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.year2018,
            'productCode': self.big_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(99000))

    def test_2018_sm_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.year2018,
            'productCode': self.sm_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(8900))

    def test_blackFriday2018_big_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.blackFriday2018,
            'productCode': self.big_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(79000))

    def test_blackFriday2018_sm_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.blackFriday2018,
            'productCode': self.sm_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(0))

    def test_2019_big_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.year2019,
            'productCode': self.big_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(119000))

    def test_2019_sm_widget__gift_card(self):
        resp = self.client.get(self.url, data={
            'date': self.year2019,
            'productCode': self.sm_widget,
            'giftCardCode': self.gift_card
        })

        self.assertEqual(resp.data['productPrice'], format_price(11500))