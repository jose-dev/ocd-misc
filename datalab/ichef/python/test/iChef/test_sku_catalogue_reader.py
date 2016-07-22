import os
import unittest
from iChef.Sku import SkuCatalogueReader

class SkuCatalogueReaderTest(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'sku_catalogue_reader.json')
        self._sku_catalogue = SkuCatalogueReader.read(filename)

    def test_count_of_sku_catalogue(self):
        sku_catalogue = self._sku_catalogue
        self.assertEqual(len(sku_catalogue.list_skus()), 4)

    def test_presence_of_sku_catalogue(self):
        sku_catalogue = self._sku_catalogue
        self.assertEqual(sku_catalogue.has_sku("sku_001"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_002"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_003"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_004"), True)
        self.assertEqual(sku_catalogue.has_sku("sku_005"), False)
        self.assertEqual(sku_catalogue.get_sku("sku_001").id, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_002").id, "sku_002")
        self.assertEqual(sku_catalogue.get_sku("sku_003").id, "sku_003")
        self.assertEqual(sku_catalogue.get_sku("sku_004").id, "sku_004")
        self.assertEqual(sku_catalogue.get_sku("sku_001").description, None)
        self.assertEqual(sku_catalogue.get_sku("sku_002").description, None)
        self.assertEqual(sku_catalogue.get_sku("sku_003").description, None)
        self.assertEqual(sku_catalogue.get_sku("sku_004").description, None)

    def test_alternatives_of_sku_catalogue(self):
        sku_catalogue = self._sku_catalogue
        self.assertEqual(len(sku_catalogue.get_sku("sku_001").alternatives), 3)
        self.assertEqual(len(sku_catalogue.get_sku("sku_002").alternatives), 2)
        self.assertEqual(len(sku_catalogue.get_sku("sku_003").alternatives), 3)
        self.assertEqual(len(sku_catalogue.get_sku("sku_004").alternatives), 2)
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].sku, "sku_001")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[0].weight, 100.0)
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[1].sku, "sku_002")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[1].weight, 0.0)
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[2].sku, "sku_003")
        self.assertEqual(sku_catalogue.get_sku("sku_001").alternatives[2].weight, 0.0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SkuCatalogueReaderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)