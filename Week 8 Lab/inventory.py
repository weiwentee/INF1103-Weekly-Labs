class Inventory:
    """
    Manages a collection of Product objects.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """
        Add a product to the inventory. Returns False if the ID already exists.
        """
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """
        Return the product with the given ID, or None if not found.
        """
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_all_products(self):
        """
        Return a copy of the product list so callers cannot modify it directly.
        """
        return list(self.__products)

    def display_all(self):
        """
        Display all products in the inventory.
        """
        if not self.__products:
            print("Inventory is empty.")
            return

        print("Current Inventory:")
        print("-------------------")
        for product in self.__products:
            product.display_information()
        print("-------------------")
