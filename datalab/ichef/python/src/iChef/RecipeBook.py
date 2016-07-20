import operator
import json

class RecipeBookReader(object):
    @staticmethod
    def read(filename=None):
        recipe_book = RecipeBook()
        with open(filename, 'r') as f:
            for line in f:
                d = json.loads(line)
                if "sku" in d:
                    recipe_book.add_entry(sku=d["sku"],
                                          sku_description=d["ingredient"],
                                          weight=d["rarity_weight"],
                                          recipe_id=d["document_no"],
                                          recipe_name=d["title"])
        return recipe_book


class Ingredient(object):
    def __init__(self, sku=None, description=None):
        self.sku = sku
        self.description = description


class RecipeIngredient(object):
    def __init__(self, sku=None, weight=0.0):
        self.sku = sku
        self.weight = weight


class Recipe(object):
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        self.ingredients = {}

    def add_ingredient(self, ingredient=None):
        self.ingredients[ingredient.sku] = ingredient

    def add_ingredients(self, ingredients=None):
        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def list_ingredients(self):
        return self.ingredients.keys()

    def has_ingredient(self, sku=None):
        return self.ingredients.has_key(sku)

    def get_ingredient(self, sku=None):
        return self.ingredients.get(sku, None)


class RecipeBook(object):
    def __init__(self):
        self.recipes = {}
        self.ingredients = {}

    def has_ingredient(self, sku=None):
        return self.ingredients.has_key(sku)

    def add_ingredient(self, ingredient=None):
        self.ingredients[ingredient.sku] = ingredient

    def add_recipe_ingredient(self, recipe_id=None, ingredient=None):
        self.recipes[recipe_id].add_ingredient(ingredient)

    def list_ingredients(self):
        return self.ingredients.keys()

    def get_ingredient(self, sku=None):
        return self.ingredients.get(sku, None)

    def has_recipe(self, recipe_id=None):
        return self.recipes.has_key(recipe_id)

    def create_recipe(self, id=None, name=None):
        self.recipes[id] = Recipe(id, name)

    def add_entry(self,sku=None, sku_description=None, weight=0.0, recipe_id=None, recipe_name=None):
        if not self.has_ingredient(sku):
            self.add_ingredient(Ingredient(sku, sku_description))
        if not self.has_recipe(recipe_id):
            self.create_recipe(recipe_id, recipe_name)
        self.add_recipe_ingredient(recipe_id, RecipeIngredient(sku, weight))

    def list_recipes(self):
        return self.recipes.keys()

    def get_recipe(self, sku=None):
        return self.recipes.get(sku, None)

    def find_recipe_with_sku(self, sku=None):
        matched = []
        for sku_item in sku.get_alternatives():
            if self.has_ingredient(sku_item.sku):
                for recipe in self.recipes.values():
                    if recipe.has_ingredient(sku_item.sku):
                        recipe_ingredient = recipe.get_ingredient(sku_item.sku)
                        matched.append(MatchedIngredient(ingredient=recipe_ingredient,
                                                         recipe=recipe.id,
                                                         basket_sku=sku.id))
            if len(matched) > 0:
                break
        return matched


class MatchedIngredient(object):
    def __init__(self, ingredient=None, basket_sku=None, recipe=None):
        self.recipe_sku = ingredient.sku
        self.weight = ingredient.weight
        self.recipe_id = recipe
        if basket_sku:
            self.set_basket_sku(basket_sku)

    def set_basket_sku(self, sku=None):
        self.basket_sku = sku
        self.is_alternative = sku != self.recipe_sku


class RecipeMatchedIngredient(object):
    def __init__(self, matched_ingredient=None):
        self.recipe_sku = matched_ingredient.recipe_sku
        self.basket_sku = matched_ingredient.basket_sku
        self.is_alternative = matched_ingredient.is_alternative
        self.weight = matched_ingredient.weight


class MatchedRecipe(Recipe):
    score = 0.0

    def update_score(self, weight=0.0):
        self.score += weight

    def add_ingredient(self, ingredient=None):
        self.ingredients[ingredient.recipe_sku] = ingredient
        self.update_score(ingredient.weight)


class MatchedRecipeList(object):
    def __init__(self, matched_ingredients=None):
        self.recipes = {}
        self.add_matched_ingredients(matched_ingredients)

    def add_matched_ingredient(self, ingredient=None):
        if not self.has_recipe(ingredient.recipe_id):
            self.create_recipe(ingredient.recipe_id)
        self.add_recipe_ingredient(ingredient.recipe_id, RecipeMatchedIngredient(ingredient))

    def add_matched_ingredients(self, ingredients=None):
        for ingredient in ingredients:
            self.add_matched_ingredient(ingredient)

    def has_recipe(self, recipe_id=None):
        return self.recipes.has_key(recipe_id)

    def create_recipe(self, id=None):
        self.recipes[id] = MatchedRecipe(id)

    def add_recipe_ingredient(self, recipe_id=None, ingredient=None):
        self.recipes[recipe_id].add_ingredient(ingredient)

    def list_recipes(self):
        return self.recipes.keys()

    def get_recipe(self, recipe_id=None):
        return self.recipes.get(recipe_id, None)

    def get_recipe_score(self, recipe_id=None):
        return self.get_recipe(recipe_id).score

    def sort_recipes_by_score(self, score=0.0):
        d = {k: self.get_recipe_score(k) for k in self.list_recipes() if self.get_recipe_score(k) >= score}
        return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    def filter_recipes_by_score(self, score=0.5):
        return self.sort_recipes_by_score(score)





