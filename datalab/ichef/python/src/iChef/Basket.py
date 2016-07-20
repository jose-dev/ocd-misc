
class BasketReader(object):
    @staticmethod
    def read(filename=None):
        basket = Basket(description="test basket")
        with open(filename, 'r') as f:
            for line in f:
                basket.add_item(BasketItem(sku=line.rstrip('\n'),
                                           quantity_amount=1))
        return basket


class BasketItem(object):
    def __init__(self, sku=None, description=None, quantity_amount=0.0, quantity_type="each"):
        self.sku = sku
        self.description = description
        self.quantity_amount = quantity_amount
        self.quantity_type = quantity_type


class Basket(object):
    def __init__(self, id=None, description=None):
        self.id = id
        self.description = description
        self.items = {}

    def add_item(self, item=None):
        self.items[item.sku] = item

    def list_items(self):
        return self.items.keys()

    def has_item(self, sku_id):
        return self.items.has_key(sku_id)

    def get_item(self, sku_id):
        return self.items.get(sku_id)

