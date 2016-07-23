import json

class SkuCatalogueReader(object):
    @staticmethod
    def read(filename=None):
        colnames = ["recipe_sku", "other_relevant_skus"]
        col_pair = [sorted(colnames), sorted(colnames, reverse=True)]

        skus = {}
        with open(filename, 'r') as f:
            for line in f:
                d = json.loads(line)
                for cols in col_pair:
                    if cols[0] not in d or cols[1] not in d:
                        continue
                    if d[cols[0]] not in skus:
                        skus[d[cols[0]]] = Sku(id=d[cols[0]])
                    skus[d[cols[0]]].add_alternative(SkuItem(sku=d[cols[1]]))

        sku_catalogue = SkuCatalogue()
        for sku_id in skus.keys():
            sku_catalogue.add_sku(skus[sku_id])
        return sku_catalogue


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

    def add_alternatives(self, sku_items=None):
        for sku_item in sku_items:
            self.add_alternative(sku_item)

    def get_alternatives(self):
        return sorted(self.alternatives, key=lambda x: x.weight, reverse=True)


class SkuCatalogue(object):
    def __init__(self):
        self.catalogue = {}

    def add_sku(self, sku=None):
        self.catalogue[sku.id] = sku

    def add_skus(self, skus=None):
        for sku in skus:
            self.add_sku(sku)

    def list_skus(self):
        return self.catalogue.keys()

    def has_sku(self, sku_id):
        return self.catalogue.has_key(sku_id)

    def get_sku(self, sku_id):
        return self.catalogue.get(sku_id)
