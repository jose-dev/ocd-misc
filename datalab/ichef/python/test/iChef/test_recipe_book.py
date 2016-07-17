import unittest
from iChef.RecipeBook import Ingredient, Recipe, RecipeBook

class RecipeBookTest(unittest.TestCase):
    def test_create_ingredient(self):
        recipe_1 = Recipe(id="recipe_001", name="test recipe 1")
        recipe_1.add_ingredient(Ingredient(sku="sku_001",
                                           description="test sku 1",
                                           weight=0.6,
                                           recipe_id="recipe_001"))
        recipe_1.add_ingredient(Ingredient(sku="sku_002",
                                           description="test sku 2",
                                           weight=0.4,
                                           recipe_id="recipe_001"))

        recipe_2 = Recipe(id="recipe_002", name="test recipe 2")
        recipe_2.add_ingredient(Ingredient(sku="sku_001",
                                           description="test sku 1",
                                           weight=0.5,
                                           recipe_id="recipe_002"))
        recipe_2.add_ingredient(Ingredient(sku="sku_002",
                                           description="test sku 2",
                                           weight=0.4,
                                           recipe_id="recipe_002"))
        recipe_2.add_ingredient(Ingredient(sku="sku_003",
                                           description="test sku 3",
                                           weight=0.1,
                                           recipe_id="recipe_002"))

        recipe_book = RecipeBook()
        recipe_book.add_recipe(recipe_1)
        recipe_book.add_recipe(recipe_2)

        self.assertEqual(len(recipe_book.list_recipes()), 2)
        self.assertEqual(recipe_book.has_recipe("recipe_001"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_002"), True)
        self.assertEqual(recipe_book.has_recipe("recipe_003"), False)

        self.assertEqual(recipe_book.get_recipe("recipe_001").id, "recipe_001")
        self.assertEqual(len(recipe_book.get_recipe("recipe_001").list_ingredients()), 2)
        self.assertEqual(recipe_book.get_recipe("recipe_002").id, "recipe_002")
        self.assertEqual(len(recipe_book.get_recipe("recipe_002").list_ingredients()), 3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeBookTest)
    unittest.TextTestRunner(verbosity=2).run(suite)