from abc import ABC, abstractmethod


class Product(ABC):
    """
    Abstract base class that represents and manages a single product.
    Cannot be instantiated directly - use PhysicalProduct or DigitalProduct.
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.update_stock(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """
        Set the stock to a new quantity. Negative stock is rejected.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """
        Display this product's common details.
        """
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """
        Return this product's common details as a dictionary for saving to JSON.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "quantity": self.__stock,
            "price": self.__price
        }

    @abstractmethod
    def get_fulfilment_info(self):
        """
        Return a message describing how this product is delivered to the customer.
        """
        pass
