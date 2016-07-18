import unittest
from iChef.Sku import SkuItem, Sku

class SkuTest(unittest.TestCase):
    def test_create_sku_without_alternatives(self):
        sku = Sku(id="sku_001", description="main sku")

        self.assertEqual(sku.id, "sku_001")
        self.assertEqual(sku.description, "main sku")
        self.assertEqual(len(sku.alternatives), 1)
        self.assertEqual(sku.alternatives[0].sku, "sku_001")
        self.assertEqual(sku.alternatives[0].description, "main sku")
        self.assertEqual(sku.alternatives[0].weight, 100.0)

    def test_create_sku_with_alternatives(self):
        sku = Sku(id="sku_001", description="main sku")
        sku.add_alternative(SkuItem(sku="sku_002",
                                    description="alternative to sku 1",
                                    weight=2.1))

        self.assertEqual(sku.id, "sku_001")
        self.assertEqual(sku.description, "main sku")
        self.assertEqual(len(sku.alternatives), 2)
        self.assertEqual(sku.alternatives[0].sku, "sku_001")
        self.assertEqual(sku.alternatives[0].description, "main sku")
        self.assertEqual(sku.alternatives[0].weight, 100.0)
        self.assertEqual(sku.alternatives[1].sku, "sku_002")
        self.assertEqual(sku.alternatives[1].description, "alternative to sku 1")
        self.assertEqual(sku.alternatives[1].weight, 2.1)


    def test_return_alternatives_sorted(self):
        sku = Sku(id="sku_001", description="main sku")
        sku.add_alternatives([SkuItem(sku="sku_002",
                                      description="alternative to sku 1",
                                      weight=2.0),
                              SkuItem(sku="sku_003",
                                      description="alternative to sku 1",
                                      weight=30.0),
                              SkuItem(sku="sku_004",
                                      description="alternative to sku 1",
                                      weight=10.0)])

        result = sku.get_alternatives()
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].sku, "sku_001")
        self.assertEqual(result[1].sku, "sku_003")
        self.assertEqual(result[2].sku, "sku_004")
        self.assertEqual(result[3].sku, "sku_002")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SkuTest)
    unittest.TextTestRunner(verbosity=2).run(suite)