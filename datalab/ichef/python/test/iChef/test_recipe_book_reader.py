import unittest
from iChef.RecipeBook import RecipeBookReader
from iChef.Sku import Sku, SkuItem
import os


class RecipeBookTest(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'recipe_book_reader.json')
        self._recipe_book = RecipeBookReader.read(filename)


    def test_create_recipe_book(self):
        recipe_book = self._recipe_book

        self.assertEqual(len(recipe_book.list_ingredients()), 3)
        self.assertEqual(recipe_book.has_ingredient("sku_001"), True)
        self.assertEqual(recipe_book.has_ingredient("sku_002"), True)
        self.assertEqual(recipe_book.has_ingredient("sku_003"), True)
        self.assertEqual(recipe_book.has_ingredient("sku_004"), False)

        self.assertEqual(recipe_book.get_ingredient("sku_001").sku, "sku_001")
        self.assertEqual(recipe_book.get_ingredient("sku_001").description, "sku 1")
        self.assertEqual(recipe_book.get_ingredient("sku_002").sku, "sku_002")
        self.assertEqual(recipe_book.get_ingredient("sku_002").description, "sku 2")
        self.assertEqual(recipe_book.get_ingredient("sku_003").sku, "sku_003")
        self.assertEqual(recipe_book.get_ingredient("sku_003").description, "sku 3")

        self.assertEqual(len(recipe_book.list_recipes()), 2)
        self.assertEqual(recipe_book.has_recipe("recipe_001"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_002"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_003"), False)

        self.assertEqual(recipe_book.get_recipe("recipe_001").id, "recipe_001")
        self.assertEqual(len(recipe_book.get_recipe("recipe_001").list_ingredients()), 2)
        self.assertEqual(recipe_book.get_recipe("recipe_002").id, "recipe_002")
        self.assertEqual(len(recipe_book.get_recipe("recipe_002").list_ingredients()), 3)


    def test_find_recipe_with_sku_in_ingredients_of_no_recipe(self):
        recipe_book = self._recipe_book
        sku = Sku(id="sku_004", description="main sku")
        result = recipe_book.find_recipe_with_sku(sku)

        self.assertEqual(len(result), 0)


    def test_find_recipe_with_sku_in_ingredients_of_one_recipe(self):
        recipe_book = self._recipe_book
        sku = Sku(id="sku_003", description="sku 3")
        result = recipe_book.find_recipe_with_sku(sku)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].recipe_sku, "sku_003")
        self.assertEqual(result[0].basket_sku, "sku_003")
        self.assertEqual(result[0].is_alternative, False)
        self.assertEqual(result[0].weight, 0.1)
        self.assertEqual(result[0].recipe_id, "recipe_002")


    def test_find_recipe_with_sku_in_ingredients_of_two_recipes(self):
        recipe_book = self._recipe_book
        sku = Sku(id="sku_001", description="sku 1")
        result = recipe_book.find_recipe_with_sku(sku)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].recipe_sku, "sku_001")
        self.assertEqual(result[0].basket_sku, "sku_001")
        self.assertEqual(result[0].is_alternative, False)
        self.assertEqual(result[0].weight, 0.6)
        self.assertEqual(result[0].recipe_id, "recipe_001")
        self.assertEqual(result[1].recipe_sku, "sku_001")
        self.assertEqual(result[0].basket_sku, "sku_001")
        self.assertEqual(result[0].is_alternative, False)
        self.assertEqual(result[1].weight, 0.5)
        self.assertEqual(result[1].recipe_id, "recipe_002")


    def test_find_recipe_with_alternative_sku_in_ingredients(self):
        recipe_book = self._recipe_book
        sku = Sku(id="sku_004", description="sku 4")
        sku.add_alternatives([SkuItem(sku="sku_002",
                                      description="alternative to sku 4",
                                      weight=2.0),
                              SkuItem(sku="sku_003",
                                      description="alternative to sku 4",
                                      weight=30.0),
                              SkuItem(sku="sku_005",
                                      description="alternative to sku 4",
                                      weight=40.0)])
        result = recipe_book.find_recipe_with_sku(sku)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].recipe_sku, "sku_003")
        self.assertEqual(result[0].basket_sku, "sku_004")
        self.assertEqual(result[0].is_alternative, True)
        self.assertEqual(result[0].weight, 0.1)
        self.assertEqual(result[0].recipe_id, "recipe_002")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeBookTest)
    unittest.TextTestRunner(verbosity=2).run(suite)