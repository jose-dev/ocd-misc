import unittest
from iChef.Sku import SkuItem

class SkuItemTest(unittest.TestCase):
    def test_create_sku_item(self):
        sku_item = SkuItem(sku="sku_001",
                           description="test sku",
                            weight=0.5)
        self.assertEqual(sku_item.sku, "sku_001")
        self.assertEqual(sku_item.description, "test sku")
        self.assertEqual(sku_item.weight, 0.5)

    def test_create_sku_item_with_default_weight(self):
        sku_item = SkuItem(sku="sku_001",
                           description="test sku")
        self.assertEqual(sku_item.sku, "sku_001")
        self.assertEqual(sku_item.description, "test sku")
        self.assertEqual(sku_item.weight, 0.0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SkuItemTest)
    unittest.TextTestRunner(verbosity=2).run(suite)