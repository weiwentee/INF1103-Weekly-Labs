from product import Product


class Inventory:
    """
    Aggregation: an Inventory groups Product objects but does not own their lifecycle.
    Products are created outside the Inventory and survive being removed from it.
    """

    def __init__(self, name: str = "Main Inventory") -> None:
        self.__name: str = name
        self.__products: list[Product] = []

    def get_name(self) -> str:
        return self.__name

    def add_product(self, product: Product) -> bool:
        """
        Add an existing Product. Returns False if the ID already exists.
        """
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """
        Remove the Product reference from this inventory and return it.
        The Product object itself is NOT destroyed.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_all_products(self) -> list[Product]:
        return list(self.__products)

    def display_all_products(self) -> None:
        """
        Polymorphism: each Product decides how to display itself.
        No isinstance() checks are needed.
        """
        if not self.__products:
            print(f"{self.__name} is empty.")
            return

        print(f"{self.__name}:")
        print("-------------------")
        for product in self.__products:
            product.display_information()
        print("-------------------")
