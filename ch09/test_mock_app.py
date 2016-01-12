import unittest
from decimal import Decimal

import mock

from app import get_orders_by_customer


class TestApp(unittest.TestCase):
    cookie_orders = [(1, u'cookiemon', u'111-111-1111')]
    cookie_details = [
        (1, u'cookiemon', u'111-111-1111',
            u'dark chocolate chip', 2, Decimal('1.00')),
        (1, u'cookiemon', u'111-111-1111',
            u'oatmeal raisin', 12, Decimal('3.00'))]

    @mock.patch('app.dal.session')
    def test_orders_by_customer_blank(self, mock_dal):
        mock_dal.query.return_value.join.return_value.filter.return_value. \
            all.return_value = []
        results = get_orders_by_customer('')
        self.assertEqual(results, [])

    @mock.patch('app.dal.session')
    def test_orders_by_customer_blank_shipped(self, mock_dal):
        mock_dal.query.return_value.join.return_value.filter.return_value. \
            filter.return_value.all.return_value = []
        results = get_orders_by_customer('', True)
        self.assertEqual(results, [])

    @mock.patch('app.dal.session')
    def test_orders_by_customer(self, mock_dal):
        mock_dal.query.return_value.join.return_value.filter.return_value. \
            all.return_value = self.cookie_orders
        results = get_orders_by_customer('cookiemon')
        self.assertEqual(results, self.cookie_orders)
