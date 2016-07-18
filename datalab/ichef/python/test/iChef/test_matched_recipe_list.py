import unittest
from iChef.RecipeBook import MatchedIngredient, RecipeIngredient, MatchedRecipeList

class MatchedRecipeListTest(unittest.TestCase):
    def test_create_matched_recipe_list(self):
        matched_ingredients = [MatchedIngredient(ingredient=RecipeIngredient(sku="sku_001", weight=0.5),
                                                 recipe="recipe_001",
                                                 basket_sku="sku_001"),
                               MatchedIngredient(ingredient=RecipeIngredient(sku="sku_002", weight=0.2),
                                                 recipe="recipe_001",
                                                 basket_sku="sku_002"),
                               MatchedIngredient(ingredient=RecipeIngredient(sku="sku_001", weight=0.2),
                                                 recipe="recipe_002",
                                                 basket_sku="sku_001")]

        matched_recipe_list = MatchedRecipeList(matched_ingredients)

        self.assertEqual(len(matched_recipe_list.list_recipes()), 2)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_001"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_002"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_003"), False)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_001").score, 0.7)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_002").score, 0.2)

        self.assertItemsEqual(matched_recipe_list.filter_recipes_by_score(), [("recipe_001", 0.7)])
        self.assertItemsEqual(matched_recipe_list.filter_recipes_by_score(0.1), [("recipe_001", 0.7), ("recipe_002", 0.2)])
        self.assertItemsEqual(matched_recipe_list.filter_recipes_by_score(0.8), [])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedRecipeListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)