import unittest
from iChef.Basket import BasketItem, Basket

class BasketTest(unittest.TestCase):
    def test_create_empty_basket(self):
        basket = Basket(description="empty basket")

        self.assertEqual(basket.id, None)
        self.assertEqual(basket.description, "empty basket")
        self.assertEqual(len(basket.list_items()), 0)

    def test_create_basket_single_item(self):
        basket_item = BasketItem(sku="sku_001",
                                 description="test sku",
                                 quantity_amount=2)
        basket = Basket(description="test basket")
        basket.add_item(basket_item)

        self.assertEqual(len(basket.list_items()), 1)
        self.assertEqual(basket.has_item("sku_001"), True)
        self.assertEqual(basket.has_item("sku_002"), False)
        self.assertEqual(basket.get_item("sku_001").sku, "sku_001")
        self.assertEqual(basket.get_item("sku_001").description, "test sku")
        self.assertEqual(basket.get_item("sku_001").quantity_amount, 2)
        self.assertEqual(basket.get_item("sku_001").quantity_type, "each")

    def test_create_basket_multiple_item(self):
        basket_item_1 = BasketItem(sku="sku_001",
                                   description="test sku",
                                   quantity_amount=2)
        basket_item_2 = BasketItem(sku="sku_002",
                                   description="test sku",
                                   quantity_amount=1)

        basket = Basket(description="test basket")
        basket.add_item(basket_item_1)
        basket.add_item(basket_item_2)

        self.assertEqual(len(basket.list_items()), 2)
        self.assertEqual(basket.has_item("sku_001"), True)
        self.assertEqual(basket.has_item("sku_002"), True)
        self.assertEqual(basket.get_item("sku_001").sku, "sku_001")
        self.assertEqual(basket.get_item("sku_001").description, "test sku")
        self.assertEqual(basket.get_item("sku_001").quantity_amount, 2)
        self.assertEqual(basket.get_item("sku_001").quantity_type, "each")
        self.assertEqual(basket.get_item("sku_002").sku, "sku_002")
        self.assertEqual(basket.get_item("sku_002").description, "test sku")
        self.assertEqual(basket.get_item("sku_002").quantity_amount, 1)
        self.assertEqual(basket.get_item("sku_002").quantity_type, "each")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BasketTest)
    unittest.TextTestRunner(verbosity=2).run(suite)