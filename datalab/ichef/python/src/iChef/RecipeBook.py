
def prepare_recipe_book(filename=None):
    """
    1- read file into dictionary
    2- create objects:
        - ingredients
        - recipe
        - recipeBook
        - recipeMatcher
    3- return recipeMatcher object


    IMPORTANT:
    -----------

    RecipeMatcher may not be needed, just recipeBook. RecipeBook object should
    be populated one ingredient entry at the time instead for a complete dictionary.


    RecipeBook could also have:
        - recipes dictionary
        - ingredients dictionary (denormalised ingredients) --> recipes dictionary may not need
            to contain all the information for the ingredients, just the if and weight
    """
    pass


class Ingredient(object):
    def __init__(self, sku=None, description=None, weight=0.0, recipe_id=None):
        self.sku = sku
        self.description = description
        self.recipe_id = recipe_id
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

    def add_recipe(self, recipe=None):
        self.recipes[recipe.id] = recipe

    def add_recipes(self, recipes=None):
        for recipe in recipes:
            self.add_recipe(recipe)

    def list_recipes(self):
        return self.recipes.keys()

    def has_recipe(self, sku=None):
        return self.recipes.has_key(sku)

    def get_recipe(self, sku=None):
        return self.recipes.get(sku, None)

    def find_recipe_with_sku(self, sku=None):
        matched = []
        for recipe in self.recipes.values():
            if recipe.has_ingredient(sku):
                matched.append(recipe.get_ingredient(sku))
        return matched


class MatchedIngredient(object):
    def __init__(self, ingredient=None, matched_sku=None):
        self.sku = ingredient.sku
        self.description = ingredient.description
        self.recipe_id = ingredient.recipe_id
        self.weight = ingredient.weight
        self.matched_sku = matched_sku
        self.is_alternative = matched_sku != ingredient.sku


class RecipeMatcher(object):
    def __init__(self, recipe_book=None):
        self.recipe_book = recipe_book

    def search_recipe_book(self, sku_alternative_list=None):
        matched = []
        for sku in sku_alternative_list:
            for ingredient in self.recipe_book.find_recipe_with_sku(sku.sku):
                matched.append(MatchedIngredient(ingredient=ingredient,
                                                 matched_sku=sku_alternative_list[0].sku))
            if len(matched) > 0:
                break
        return matched


class MatchedRecipe(object):
    """

        TODO

        Implement MatchedRecipe class to collect the MatchedIngredient objects and group
        them into recipes to calculate total score and also to organise ingredients into
        found/missing in basket.

    """
    pass




