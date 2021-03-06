import unittest
from iChef.RecipeBook import RecipeIngredient, Recipe

class RecipeTest(unittest.TestCase):
    def test_create_recipe(self):
        recipe = Recipe(id="recipe_001", name="test recipe")
        recipe.add_ingredient(RecipeIngredient(sku="sku_001", weight=0.6))
        recipe.add_ingredient(RecipeIngredient(sku="sku_002", weight=0.4))

        self.assertEqual(recipe.recipe_id, "recipe_001")
        self.assertEqual(recipe.name, "test recipe")
        self.assertEqual(len(recipe.list_ingredients()), 2)
        self.assertEqual(len(recipe.list_ingredients()), 2)
        self.assertEqual(recipe.has_ingredient("sku_001"), True)
        self.assertEqual(recipe.has_ingredient("sku_002"), True)
        self.assertEqual(recipe.has_ingredient("sku_003"), False)
        self.assertEqual(recipe.get_ingredient("sku_001").sku, "sku_001")
        self.assertEqual(recipe.get_ingredient("sku_001").weight, 0.6)
        self.assertEqual(recipe.get_ingredient("sku_002").sku, "sku_002")
        self.assertEqual(recipe.get_ingredient("sku_002").weight, 0.4)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeTest)
    unittest.TextTestRunner(verbosity=2).run(suite)