import unittest
from iChef.RecipeBook import MatchedIngredient, RecipeIngredient, MatchedRecipeList

class MatchedRecipeListTest(unittest.TestCase):
    def setUp(self):
        matched_ingredients = [MatchedIngredient(ingredient=RecipeIngredient(sku="sku_001", weight=0.5),
                                                 recipe="recipe_001",
                                                 basket_sku="sku_001"),
                               MatchedIngredient(ingredient=RecipeIngredient(sku="sku_002", weight=0.2),
                                                 recipe="recipe_001",
                                                 basket_sku="sku_002"),
                               MatchedIngredient(ingredient=RecipeIngredient(sku="sku_001", weight=0.2),
                                                 recipe="recipe_002",
                                                 basket_sku="sku_001")]
        self._matched_ingredients = matched_ingredients

    def test_create_matched_recipe_list(self):
        matched_recipe_list = MatchedRecipeList(self._matched_ingredients)

        self.assertEqual(len(matched_recipe_list.list_recipes()), 2)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_001"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_002"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_003"), False)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_001").score, 0.7)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_002").score, 0.2)

    def test_filter_matched_recipes_returns_empty_list(self):
        matched_recipe_list = MatchedRecipeList(self._matched_ingredients)
        self.assertItemsEqual(matched_recipe_list.filter_recipes_by_score(0.8), [])

    def test_filter_matched_recipes_returns_only_one(self):
        matched_recipe_list = MatchedRecipeList(self._matched_ingredients)
        self.assertItemsEqual(matched_recipe_list.filter_recipes_by_score(), [("recipe_001", 0.7)])

    def test_filter_matched_recipes_returns_several_ordered_entries(self):
        matched_recipe_list = MatchedRecipeList(self._matched_ingredients)
        result = matched_recipe_list.filter_recipes_by_score(0.1)
        self.assertEqual(len(result), 2)
        self.assertItemsEqual(result[0], ("recipe_001", 0.7))
        self.assertItemsEqual(result[1], ("recipe_002", 0.2))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedRecipeListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)