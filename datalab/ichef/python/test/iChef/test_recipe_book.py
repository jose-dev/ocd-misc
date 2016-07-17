import unittest
from iChef.RecipeBook import Ingredient, Recipe, RecipeBook

class RecipeBookTest(unittest.TestCase):
    def setUp(self):
        recipe_1 = Recipe(id="recipe_001", name="test recipe 1")
        recipe_1.add_ingredients([Ingredient(sku="sku_001",
                                             description="test sku 1",
                                             weight=0.6,
                                             recipe_id="recipe_001"),
                                  Ingredient(sku="sku_002",
                                             description="test sku 2",
                                             weight=0.4,
                                             recipe_id="recipe_001")])

        recipe_2 = Recipe(id="recipe_002", name="test recipe 2")
        recipe_2.add_ingredients([Ingredient(sku="sku_001",
                                             description="test sku 1",
                                             weight=0.5,
                                             recipe_id="recipe_002"),
                                  Ingredient(sku="sku_002",
                                             description="test sku 2",
                                             weight=0.4,
                                             recipe_id="recipe_002"),
                                  Ingredient(sku="sku_003",
                                             description="test sku 3",
                                             weight=0.1,
                                             recipe_id="recipe_002")])

        self._recipes = [recipe_1, recipe_2]

    def test_create_recipe_book(self):
        recipe_book = RecipeBook()
        recipe_book.add_recipes(self._recipes)

        self.assertEqual(len(recipe_book.list_recipes()), 2)
        self.assertEqual(recipe_book.has_recipe("recipe_001"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_002"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_003"), False)

        self.assertEqual(recipe_book.get_recipe("recipe_001").id, "recipe_001")
        self.assertEqual(len(recipe_book.get_recipe("recipe_001").list_ingredients()), 2)
        self.assertEqual(recipe_book.get_recipe("recipe_002").id, "recipe_002")
        self.assertEqual(len(recipe_book.get_recipe("recipe_002").list_ingredients()), 3)


    def test_find_recipe_with_sku_in_ingredients_of_one_recipe(self):
        recipe_book = RecipeBook()
        recipe_book.add_recipes(self._recipes)
        result = recipe_book.find_recipe_with_sku("sku_003")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].sku, "sku_003")
        self.assertEqual(result[0].description, "test sku 3")
        self.assertEqual(result[0].weight, 0.1)
        self.assertEqual(result[0].recipe_id, "recipe_002")


    def test_find_recipe_with_sku_in_ingredients_of_two_recipes(self):
        recipe_book = RecipeBook()
        recipe_book.add_recipes(self._recipes)
        result = recipe_book.find_recipe_with_sku("sku_001")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].sku, "sku_001")
        self.assertEqual(result[0].description, "test sku 1")
        self.assertEqual(result[0].weight, 0.6)
        self.assertEqual(result[0].recipe_id, "recipe_001")
        self.assertEqual(result[1].sku, "sku_001")
        self.assertEqual(result[1].description, "test sku 1")
        self.assertEqual(result[1].weight, 0.5)
        self.assertEqual(result[1].recipe_id, "recipe_002")


    def test_find_recipe_with_sku_in_ingredients_of_no_recipe(self):
        recipe_book = RecipeBook()
        recipe_book.add_recipes(self._recipes)
        result = recipe_book.find_recipe_with_sku("sku_004")

        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeBookTest)
    unittest.TextTestRunner(verbosity=2).run(suite)