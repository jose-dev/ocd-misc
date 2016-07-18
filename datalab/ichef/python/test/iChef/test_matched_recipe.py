import unittest
from iChef.RecipeBook import RecipeMatchedIngredient, MatchedRecipe, RecipeIngredient, MatchedIngredient

class MatchedRecipeTest(unittest.TestCase):
    def test_create_recipe(self):
        recipe_matched_ingredients = [RecipeMatchedIngredient(MatchedIngredient(ingredient=RecipeIngredient(sku="sku_001",
                                                                                                            weight=0.5),
                                                                                basket_sku="sku_001")),
                                      RecipeMatchedIngredient(MatchedIngredient(ingredient=RecipeIngredient(sku="sku_002",
                                                                                                            weight=0.2),
                                                                                basket_sku="sku_003"))]

        matched_recipe = MatchedRecipe(id="recipe_001")
        matched_recipe.add_ingredients(recipe_matched_ingredients)

        self.assertEqual(matched_recipe.id, "recipe_001")
        self.assertEqual(matched_recipe.name, None)
        self.assertEqual(len(matched_recipe.list_ingredients()), 2)
        self.assertEqual(matched_recipe.has_ingredient("sku_001"), True)
        self.assertEqual(matched_recipe.has_ingredient("sku_002"), True)
        self.assertEqual(matched_recipe.has_ingredient("sku_003"), False)
        self.assertEqual(matched_recipe.get_ingredient("sku_001").recipe_sku, "sku_001")
        self.assertEqual(matched_recipe.get_ingredient("sku_001").basket_sku, "sku_001")
        self.assertEqual(matched_recipe.get_ingredient("sku_001").is_alternative, False)
        self.assertEqual(matched_recipe.get_ingredient("sku_001").weight, 0.5)
        self.assertEqual(matched_recipe.get_ingredient("sku_002").recipe_sku, "sku_002")
        self.assertEqual(matched_recipe.get_ingredient("sku_002").basket_sku, "sku_003")
        self.assertEqual(matched_recipe.get_ingredient("sku_002").is_alternative, True)
        self.assertEqual(matched_recipe.get_ingredient("sku_002").weight, 0.2)
        self.assertEqual(matched_recipe.score, 0.7)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedRecipeTest)
    unittest.TextTestRunner(verbosity=2).run(suite)