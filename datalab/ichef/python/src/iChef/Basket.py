def prepare_backet(filename=None):
    """
    1- read file into dictionary
    2- create objects:
        - basket item
        - basket
    3- return basket object
    """
    pass


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

