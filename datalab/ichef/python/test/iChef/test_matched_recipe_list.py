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
                                                 basket_sku="sku_003")]
        matched_recipe_list = MatchedRecipeList()
        matched_recipe_list.add_entries(matched_ingredients)
        self._matched_recipe_list = matched_recipe_list

    def test_create_matched_recipe_list(self):
        matched_recipe_list = self._matched_recipe_list

        self.assertEqual(len(matched_recipe_list.list_recipes()), 2)
        self.assertEqual(len(matched_recipe_list.list_ingredients()), 3)
        self.assertItemsEqual(matched_recipe_list.list_ingredients(), ["sku_001", "sku_002", "sku_003"])
        self.assertEqual(matched_recipe_list.has_recipe("recipe_001"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_002"), True)
        self.assertEqual(matched_recipe_list.has_recipe("recipe_003"), False)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_001").score, 0.7)
        self.assertEqual(matched_recipe_list.get_recipe("recipe_002").score, 0.2)

    def test_filter_matched_recipes_returns_empty_list(self):
        matched_recipe_list = self._matched_recipe_list
        filtered_recipe_list = matched_recipe_list.filter_recipes_by_score(0.8)
        self.assertEqual(len(filtered_recipe_list.list_recipes()), 0)
        self.assertEqual(len(filtered_recipe_list.list_ingredients()), 0)

    def test_filter_matched_recipes_returns_only_one(self):
        matched_recipe_list = self._matched_recipe_list
        filtered_recipe_list = matched_recipe_list.filter_recipes_by_score(0.7)
        self.assertEqual(len(filtered_recipe_list.list_recipes()), 1)
        self.assertEqual(len(filtered_recipe_list.list_ingredients()), 2)
        self.assertEqual(filtered_recipe_list.has_recipe("recipe_001"), True)
        self.assertEqual(filtered_recipe_list.has_recipe("recipe_002"), False)
        self.assertEqual(filtered_recipe_list.get_recipe("recipe_001").score, 0.7)

    def test_filter_matched_recipes_returns_several_ordered_entries(self):
        matched_recipe_list = self._matched_recipe_list
        filtered_recipe_list = matched_recipe_list.filter_recipes_by_score(0.1)
        self.assertEqual(len(filtered_recipe_list.list_recipes()), 2)
        self.assertEqual(len(filtered_recipe_list.list_ingredients()), 3)
        self.assertItemsEqual(filtered_recipe_list.list_ingredients(), ["sku_001", "sku_002", "sku_003"])
        self.assertEqual(filtered_recipe_list.has_recipe("recipe_001"), True)
        self.assertEqual(filtered_recipe_list.has_recipe("recipe_002"), True)
        self.assertEqual(filtered_recipe_list.has_recipe("recipe_003"), False)
        self.assertEqual(filtered_recipe_list.get_recipe("recipe_001").score, 0.7)
        self.assertEqual(filtered_recipe_list.get_recipe("recipe_002").score, 0.2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatchedRecipeListTest)
    unittest.TextTestRunner(verbosity=2).run(suite)