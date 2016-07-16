
def prepare_recipe_book(filename=None):
    """
    1- read file into dictionary
    2- create objects:
        - ingredients
        - recipe
        - recipeBook
    3- return recipeBook object
    """
    pass


class MatchedIngredient(object):
    def __init__(self, ingredient=None, matched_sku=None):
        self.sku = ingredient.sku
        self.description = ingredient.description
        self.recipe_id = ingredient.recipe_id
        self.weight = ingredient.weight
        self.matched_sku = matched_sku
        self.is_alternative = matched_sku == ingredient.sku


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

    def has_ingredient(self, sku=None):
        return self.ingredients.has_key(sku)

    def get_ingredient(self, sku=None):
        return self.ingredients.get(sku, None)


class RecipeBook(object):
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, recipe=None):
        self.recipes[recipe.id] = recipe

    def find_recipe_with_sku(self, sku=None):
        matched = []
        for recipe in self.recipes.values():
            if recipe.has_ingredient(sku):
                matched.append(MatchedIngredient(ingredient=recipe.get_ingredient(sku),
                                                 matched_sku=sku))
        return matched