import os
import unittest
from iChef.Basket import BasketItem, BasketReader

class BasketReaderTest(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'basket_reader.json')
        self._basket = BasketReader.read(filename)

    def test_basket_content(self):
        basket = self._basket

        self.assertEqual(len(basket.list_items()), 2)
        self.assertEqual(basket.has_item("sku_001"), True)
        self.assertEqual(basket.has_item("sku_002"), True)
        self.assertEqual(basket.has_item("sku_003"), False)
        self.assertEqual(basket.get_item("sku_001").sku, "sku_001")
        self.assertEqual(basket.get_item("sku_001").description, None)
        self.assertEqual(basket.get_item("sku_001").quantity_amount, 1)
        self.assertEqual(basket.get_item("sku_001").quantity_type, "each")
        self.assertEqual(basket.get_item("sku_002").sku, "sku_002")
        self.assertEqual(basket.get_item("sku_002").description, None)
        self.assertEqual(basket.get_item("sku_002").quantity_amount, 1)
        self.assertEqual(basket.get_item("sku_002").quantity_type, "each")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BasketReaderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)