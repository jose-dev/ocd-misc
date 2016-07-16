
def prepare_sku(filename=None):
    """
    1- read file into dictionary
    2- create objects:
        - sku as a list of alternatives with main sku at top
        - sku list
    3- return sku list object
    """
    pass


class SkuItem(object):
    def __init__(self, sku=None, description=None, weight=0.0):
        self.sku = sku
        self.description = description
        self.weight = weight

class Sku(object):
    MAX_SCORE = 100.0

    def __init__(self, id=None, description=None):
        self.id = id
        self.description = description
        self.alternatives = []
        self.add_alterative(SkuItem(sku=self.id,
                                    description=self.description,
                                    weight=self.MAX_SCORE))

    def add_alterative(self, sku_item=None):
        self.alternatives.append(sku_item)



class SkuCatalogue(object):
    def __init__(self):
        self.catalogue = {}

    def add_sku(self, sku=None):
        self.catalogue[sku.id] = sku

    def has_ingredient(self, sku=None):
        return self.ingredients.has_key(sku)

    def get_ingredient(self, sku=None):
        return self.ingredients.get(sku, None)

