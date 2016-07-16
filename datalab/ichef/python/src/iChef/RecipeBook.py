
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

    def find_recipe_ingredient_for_sku(self, sku=None):
        matched = []
        for recipe in self.recipes.values():
            if recipe.has_ingredient(sku):
                matched.append(recipe.get_ingredient(sku))
        return matched