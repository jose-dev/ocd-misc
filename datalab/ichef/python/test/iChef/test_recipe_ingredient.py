import unittest
from iChef.RecipeBook import RecipeIngredient

class RecipeIngredientTest(unittest.TestCase):
    def test_create_recipe_ingredient(self):
        ingredient = RecipeIngredient(sku="sku_001", weight=0.5)
        self.assertEqual(ingredient.sku, "sku_001")
        self.assertEqual(ingredient.weight, 0.5)

    def test_create_recipe_ingredient_with_default_weight(self):
        ingredient = RecipeIngredient(sku="sku_001")
        self.assertEqual(ingredient.sku, "sku_001")
        self.assertEqual(ingredient.weight, 0.0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeIngredientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)