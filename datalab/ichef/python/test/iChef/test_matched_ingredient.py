import unittest
from iChef.RecipeBook import MatchedIngredient, Ingredient

class MatchedIngredientTest(unittest.TestCase):
    def test_create_matched_ingredient(self):
        ingredient = Ingredient(sku="sku_001",
                                description="test sku",
                                weight=0.5,
                                recipe_id="recipe_001")
        matched_ingredient = MatchedIngredient(ingredient=ingredient,
                                               matched_sku="sku_001")

        self.assertEqual(matched_ingredient.sku, "sku_001")
        self.assertEqual(matched_ingredient.description, "test sku")
        self.assertEqual(matched_ingredient.weight, 0.5)
        self.assertEqual(matched_ingredient.recipe_id, "recipe_001")
        self.assertEqual(matched_ingredient.matched_sku, "sku_001")
        self.assertEqual(matched_ingredient.is_alternative, False)

    def test_create_matched_ingredient_with_alternative(self):
        ingredient = Ingredient(sku="sku_001",
                                description="test sku",
                                weight=0.5,
                                recipe_id="recipe_001")
        matched_ingredient = MatchedIngredient(ingredient=ingredient,
                                               matched_sku="sku_002")

        self.assertEqual(matched_ingredient.sku, "sku_001")
        self.assertEqual(matched_ingredient.description, "test sku")
        self.assertEqual(matched_ingredient.weight, 0.5)
        self.assertEqual(matched_ingredient.recipe_id, "recipe_001")
        self.assertEqual(matched_ingredient.matched_sku, "sku_002")
        self.assertEqual(matched_ingredient.is_alternative, True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedIngredientTest)
    unittest.TextTestRunner(verbosity=2).run(suite)