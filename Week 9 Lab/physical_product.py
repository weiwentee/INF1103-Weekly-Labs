from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """
    A product that has a weight and must be physically shipped.
    Inherits from Product and implements the CanBeShipped interface.
    """

    BASE_SHIPPING_FEE = 5.00
    RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        """
        Display the common product details, then the physical-specific details.
        """
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return f"'{self.get_name()}' requires physical shipping."

    def calculate_shipping_cost(self):
        """
        Shipping cost = base fee + rate per kg of weight.
        """
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
