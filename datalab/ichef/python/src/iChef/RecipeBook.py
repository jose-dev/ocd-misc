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
        self.recipe_id = id
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


class _RecipeBookBase(object):
    def __init__(self):
        self.recipes = {}
        self.ingredients = {}
        self.recipe_ingredients = {}

    def has_ingredient(self, sku=None):
        return self.ingredients.has_key(sku)

    def add_ingredient(self, ingredient=None):
        self.ingredients[ingredient.sku] = ingredient
        self.recipe_ingredients[ingredient.sku] = {}

    def add_recipe_ingredient(self, recipe_id=None, ingredient=None):
        self.recipes[recipe_id].add_ingredient(ingredient)
        self.recipe_ingredients[ingredient.sku][recipe_id] = True

    def list_ingredients(self):
        return self.ingredients.keys()

    def get_ingredient(self, sku=None):
        return self.ingredients.get(sku, None)

    def has_recipe(self, recipe_id=None):
        return self.recipes.has_key(recipe_id)

    def add_recipe(self, recipe=None):
        self.recipes[recipe.recipe_id] = recipe

    def list_recipes(self):
        return self.recipes.keys()

    def get_recipe(self, recipe_id=None):
        return self.recipes.get(recipe_id, None)

    def list_recipe_ingredients(self):
        return self.recipe_ingredients.keys()

    def get_recipe_ingredient(self, sku_id=None):
        return self.recipe_ingredients.get(sku_id, None)

    def add_entries(self, entries=None):
        for entry in entries:
            self.add_entry(entry)

    def add_entry(self):
        raise (NotImplementedError)


class RecipeBook(_RecipeBookBase):
    def add_entry(self,sku=None, sku_description=None, weight=0.0, recipe_id=None, recipe_name=None):
        if not self.has_ingredient(sku):
            self.add_ingredient(Ingredient(sku, sku_description))
        if not self.has_recipe(recipe_id):
            self.add_recipe(Recipe(recipe_id, recipe_name))
        self.add_recipe_ingredient(recipe_id, RecipeIngredient(sku, weight))

    def find_recipe_with_sku(self, sku=None):
        matched = []
        for sku_item in sku.get_alternatives():
            if self.has_ingredient(sku_item.sku):
                for recipe_id in self.recipe_ingredients[sku_item.sku].keys():
                    recipe = self.get_recipe(recipe_id)
                    recipe_ingredient = recipe.get_ingredient(sku_item.sku)
                    matched.append(MatchedIngredient(ingredient=recipe_ingredient,
                                                     recipe=recipe.recipe_id,
                                                     basket_sku=sku.id))
            if len(matched) > 0:
                break
        return matched


class MatchedIngredient(object):
    def __init__(self, ingredient=None, basket_sku=None, recipe=None):
        self.recipe_sku = ingredient.sku
        self.weight = ingredient.weight
        self.recipe_id = recipe
        self.basket_sku = basket_sku
        self.is_alternative = self.basket_sku != self.recipe_sku


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
        if ingredient.recipe_sku not in self.ingredients:
            self.ingredients[ingredient.recipe_sku] = ingredient
            self.update_score(ingredient.weight)


class MatchedRecipeList(_RecipeBookBase):
    def add_entry(self, ingredient=None):
        if not self.has_ingredient(ingredient.basket_sku):
            self.add_ingredient(Ingredient(ingredient.basket_sku))
        if not self.has_recipe(ingredient.recipe_id):
            self.add_recipe(MatchedRecipe(ingredient.recipe_id))
        self.add_recipe_ingredient(ingredient.recipe_id, RecipeMatchedIngredient(ingredient))

    def add_recipe_ingredient(self, recipe_id=None, ingredient=None):
        self.recipes[recipe_id].add_ingredient(ingredient)
        self.recipe_ingredients[ingredient.basket_sku][recipe_id] = True

    def get_recipe_score(self, recipe_id=None):
        return self.get_recipe(recipe_id).score

    def sort_recipes_by_score(self, cutoff=0.0):
        d = {k: self.get_recipe_score(k) for k in self.list_recipes() if self.get_recipe_score(k) >= cutoff}
        return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    def filter_recipes_by_score(self, cutoff=0.5):
        selected_recipe_list = MatchedRecipeList()
        for recipe_pairs in self.sort_recipes_by_score(cutoff):
            recipe_id = recipe_pairs[0]
            for sku_id in self.get_recipe(recipe_id).list_ingredients():
                ingredient = self.get_recipe(recipe_id).get_ingredient(sku_id)
                selected_recipe_list.add_entry(MatchedIngredient(ingredient=RecipeIngredient(sku=ingredient.recipe_sku,
                                                                                             weight=ingredient.weight),
                                                                basket_sku=ingredient.basket_sku,
                                                                recipe=recipe_id))
        return selected_recipe_list










