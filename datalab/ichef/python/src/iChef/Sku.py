
def prepare_sku(filename=None):
    """
    1- read file into dictionary
    2- create objects:
        - sku as a list of alternatives with main sku at top
        - sku catalogue
    3- return sku catalogue object
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
        self.add_alternative(SkuItem(sku=self.id,
                                     description=self.description,
                                     weight=self.MAX_SCORE))

    def add_alternative(self, sku_item=None):
        self.alternatives.append(sku_item)


class SkuCatalogue(object):
    def __init__(self):
        self.catalogue = {}

    def add_sku(self, sku=None):
        self.catalogue[sku.id] = sku

    def list_skus(self):
        return self.catalogue.keys()

    def has_sku(self, sku_id):
        return self.catalogue.has_key(sku_id)

    def get_sku(self, sku_id):
        return self.catalogue.get(sku_id)
