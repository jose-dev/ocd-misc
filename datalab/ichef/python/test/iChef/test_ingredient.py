import unittest
from iChef.RecipeBook import Ingredient

class IngredientTest(unittest.TestCase):
    def test_create_ingredient(self):
        ingredient = Ingredient(sku="sku_001",
                                description="test sku",
                                weight=0.5,
                                recipe_id="recipe_001")
        self.assertEqual(ingredient.sku, "sku_001")
        self.assertEqual(ingredient.description, "test sku")
        self.assertEqual(ingredient.weight, 0.5)
        self.assertEqual(ingredient.recipe_id, "recipe_001")

    def test_create_ingredient_with_default_weight(self):
        ingredient = Ingredient(sku="sku_001",
                                description="test sku",
                                recipe_id="recipe_001")
        self.assertEqual(ingredient.sku, "sku_001")
        self.assertEqual(ingredient.description, "test sku")
        self.assertEqual(ingredient.weight, 0.0)
        self.assertEqual(ingredient.recipe_id, "recipe_001")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(IngredientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)