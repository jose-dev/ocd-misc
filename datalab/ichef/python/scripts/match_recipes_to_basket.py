from iChef.RecipeBook import RecipeBookReader
from iChef.Basket import BasketReader
from iChef.Sku import SkuCatalogueReader
import pprint

def main():
    recipe_book_filename   = 'recipe_ingredient_rarity_weights.json'
    basket_filename        = 'devanshi_summer.txt'
    sku_catalogue_filename = 'dp_other_relevant_skus.json'

    o_recipe_book   = RecipeBookReader.read(recipe_book_filename)
    o_basket        = BasketReader.read(basket_filename)
    o_sku_catalogue = SkuCatalogueReader.read(sku_catalogue_filename)

    pprint.pprint(o_recipe_book.get_recipe("1000421").__dict__)
    pprint.pprint(o_basket.get_item("12074011").__dict__)
    pprint.pprint(o_sku_catalogue.get_sku("12074011").__dict__)

if __name__ == '__main__':
    main()

