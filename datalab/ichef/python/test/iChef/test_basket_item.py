import unittest
from iChef.Basket import BasketItem

class BasketItemTest(unittest.TestCase):
    def test_create_basket_item(self):
        basket_item = BasketItem(sku="sku_001",
                                 description="test sku",
                                 quantity_amount=0.5,
                                 quantity_type="kilo")
        self.assertEqual(basket_item.sku, "sku_001")
        self.assertEqual(basket_item.description, "test sku")
        self.assertEqual(basket_item.quantity_amount, 0.5)
        self.assertEqual(basket_item.quantity_type, "kilo")

    def test_create_basket_item_with_default_type(self):
        basket_item = BasketItem(sku="sku_001",
                                 description="test sku",
                                 quantity_amount=2)
        self.assertEqual(basket_item.sku, "sku_001")
        self.assertEqual(basket_item.description, "test sku")
        self.assertEqual(basket_item.quantity_amount, 2)
        self.assertEqual(basket_item.quantity_type, "each")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BasketItemTest)
    unittest.TextTestRunner(verbosity=2).run(suite)