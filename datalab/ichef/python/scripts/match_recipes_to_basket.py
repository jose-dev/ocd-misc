import os
import argparse
import logging
import pprint
from iChef.RecipeBook import RecipeBookReader, MatchedRecipeList
from iChef.Basket import BasketReader
from iChef.Sku import SkuCatalogueReader


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCORE = 0.5
RECIPE_BOOK_FILENAME   = os.path.join(SCRIPT_PATH, 'resources', 'recipe_ingredient_rarity_weights.json')
SKU_CATALOGUE_FILENAME = os.path.join(SCRIPT_PATH, 'resources', 'dp_other_relevant_skus.json')


################################################################################

def arg_parser():
    parser = argparse.ArgumentParser(description='Transfer test data from local disk to cloud.')
    parser.add_argument('-r', '--recipe_book',   type=str,   help='File with recipe book.   Default: {}'.format(RECIPE_BOOK_FILENAME),   default=RECIPE_BOOK_FILENAME)
    parser.add_argument('-c', '--sku_catalogue', type=str,   help='File with sku catalogue. Default: {}'.format(SKU_CATALOGUE_FILENAME), default=SKU_CATALOGUE_FILENAME)
    parser.add_argument('-s', '--score',         type=float, help='Minimum recipe score.    Default: {}'.format(str(DEFAULT_SCORE)),     default=DEFAULT_SCORE)
    parser.add_argument('-b', '--basket',        required=True, type=str, help='Input basket file')
    #parser.add_argument('-o', '--output_file', required=True, type=str, help='Name of output file')
    parser.add_argument('-k', '--skip_basket',  action='store_true', help='Input basket file. Default: FALSE', default=False)

    args = parser.parse_args()
    return vars(args)


################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s -- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    logging.info("Validating arguments...")
    cmdargs = arg_parser()
    recipe_book_filename = cmdargs['recipe_book']
    basket_filename = cmdargs['basket']
    sku_catalogue_filename = cmdargs['sku_catalogue']
    score = cmdargs['score']
    skip_basket = cmdargs['skip_basket']

    logging.info("Reading Data...")
    o_basket        = BasketReader.read(basket_filename)
    o_sku_catalogue = SkuCatalogueReader.read(sku_catalogue_filename)
    o_recipe_book   = RecipeBookReader.read(recipe_book_filename)

    logging.info("Running predictions...")
    matched_recipe_list = MatchedRecipeList()
    for sku_id in o_basket.list_items():
        if o_sku_catalogue.has_sku(sku_id):
            sku = o_sku_catalogue.get_sku(sku_id)
            matched = o_recipe_book.find_recipe_with_sku(sku)
            if len(matched) > 0:
                matched_recipe_list.add_entries(matched)

    logging.info("Selecting predictions for given score...")
    selected_recipe_list = matched_recipe_list.filter_recipes_by_score(score)

    logging.info("Printing predicted recipes...")
    print('\n')
    print('\t'.join(['RECIPE ID', 'SCORE', 'RECIPE NAME']))
    for selected_recipe in selected_recipe_list.sort_recipes_by_score():
        print('\t'.join([selected_recipe[0],
                         str(selected_recipe[1]),
                         o_recipe_book.get_recipe(selected_recipe[0]).name]))
    print('\n')

    if not skip_basket:
        logging.info("Printing basket...")
        print('\n')
        print('\t'.join(['SKU ID', 'RECIPE IDS', 'SKU NAME']))
        for sku_id in o_basket.list_items():
            recipe_ids = "no_recipe"
            sku_name   = "no description"
            if selected_recipe_list.has_ingredient(sku_id):
                recipe_ids = ','.join(selected_recipe_list.get_recipe_ingredient(sku_id))
            if o_recipe_book.has_ingredient(sku_id):
                sku_name   = o_recipe_book.get_ingredient(sku_id).description
            print('\t'.join([sku_id,
                             recipe_ids,
                             sku_name]))
        print('\n')


    logging.info("All done")


if __name__ == '__main__':
    main()

