import unittest
from iChef.RecipeBook import MatchedIngredient, RecipeIngredient

class MatchedIngredientTest(unittest.TestCase):
    def test_create_matched_ingredient(self):
        ingredient = RecipeIngredient(sku="sku_001", weight=0.5)
        matched_ingredient = MatchedIngredient(ingredient=ingredient,
                                               recipe="recipe_001",
                                               basket_sku="sku_001")

        self.assertEqual(matched_ingredient.recipe_sku, "sku_001")
        self.assertEqual(matched_ingredient.weight, 0.5)
        self.assertEqual(matched_ingredient.recipe_id, "recipe_001")
        self.assertEqual(matched_ingredient.basket_sku, "sku_001")
        self.assertEqual(matched_ingredient.is_alternative, False)

    def test_create_matched_ingredient_with_alternative(self):
        ingredient = RecipeIngredient(sku="sku_001", weight=0.5)
        matched_ingredient = MatchedIngredient(ingredient=ingredient,
                                               recipe="recipe_001",
                                               basket_sku="sku_002")

        self.assertEqual(matched_ingredient.recipe_sku, "sku_001")
        self.assertEqual(matched_ingredient.weight, 0.5)
        self.assertEqual(matched_ingredient.recipe_id, "recipe_001")
        self.assertEqual(matched_ingredient.basket_sku, "sku_002")
        self.assertEqual(matched_ingredient.is_alternative, True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedIngredientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)