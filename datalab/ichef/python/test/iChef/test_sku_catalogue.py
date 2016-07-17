import unittest
from iChef.Sku import SkuItem, Sku, SkuCatalogue

class SkuCatalogueTest(unittest.TestCase):
    def test_create_sku_catalogue_with_single_sku(self):
        sku_catalogue = SkuCatalogue()
        sku_catalogue.add_sku(Sku(id="sku_001", description="main sku"))

        self.assertEqual(len(sku_catalogue.list_skus()), 1)
        self.assertEqual(sku_catalogue.has_sku("sku_001"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_002"), False)
        self.assertEqual(sku_catalogue.get_sku("sku_001").id, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_001").description, "main sku")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].sku, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].description, "main sku")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].weight, 100.0)


    def test_create_sku_catalogue_with_two_sku(self):
        sku_catalogue = SkuCatalogue()
        sku_catalogue.add_skus([Sku(id="sku_001", description="main sku 1"),
                                Sku(id="sku_002", description="main sku 2")])

        self.assertEqual(len(sku_catalogue.list_skus()), 2)
        self.assertEqual(sku_catalogue.has_sku("sku_001"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_002"), True)
        self.assertEqual(sku_catalogue.get_sku("sku_001").id, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_001").description, "main sku 1")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].sku, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].description, "main sku 1")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].weight, 100.0)
        self.assertEqual(sku_catalogue.get_sku("sku_002").id, "sku_002")
        self.assertEqual(sku_catalogue.get_sku("sku_002").description, "main sku 2")
        self.assertEqual(sku_catalogue.get_sku("sku_002").alternatives[0].sku, "sku_002")
        self.assertEqual(sku_catalogue.get_sku("sku_002").alternatives[0].description, "main sku 2")
        self.assertEqual(sku_catalogue.get_sku("sku_002").alternatives[0].weight, 100.0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SkuCatalogueTest)
    unittest.TextTestRunner(verbosity=2).run(suite)