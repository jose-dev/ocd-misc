import unittest
from iChef.RecipeBook import Ingredient

class IngredientTest(unittest.TestCase):
    def test_create_ingredient(self):
        ingredient = Ingredient(sku="sku_001",
                                description="test sku")
        self.assertEqual(ingredient.sku, "sku_001")
        self.assertEqual(ingredient.description, "test sku")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(IngredientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)