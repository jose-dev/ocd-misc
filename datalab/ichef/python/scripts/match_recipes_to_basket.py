from iChef.RecipeBook import RecipeBookReader
import pprint

def main():
    recipe_book_filename = 'recipe_ingredient_rarity_weights.json'
    o_recipe_book = RecipeBookReader.read(recipe_book_filename)

    pprint.pprint(o_recipe_book.get_recipe("1000421").__dict__)



if __name__ == '__main__':
    main()

