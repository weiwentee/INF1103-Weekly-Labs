from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """
    Abstract base class that represents and manages a single product.
    Each Product is associated with one Supplier (association, not ownership).
    Product owns the price and stock rules, so every subclass inherits them (LSP).
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = 0.0
        self.__stock: int = 0
        self.__supplier: Supplier = supplier
        self.set_price(price)
        self.update_stock(stock)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def set_price(self, price: float) -> None:
        """
        Validation: a price must be greater than zero.
        float() itself raises ValueError for text such as "abc".
        """
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__price = price

    def update_stock(self, quantity: int) -> None:
        """
        Set the stock to a new quantity. Negative stock is rejected.
        Every subclass must preserve this meaning (LSP).
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print(f"    Supplier: {self.__supplier.get_name()} ({self.__supplier.get_contact_email()})")

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "quantity": self.__stock,
            "price": self.__price,
            "supplier": self.__supplier.to_dict()
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """
        Return a message describing how this product is delivered to the customer.
        """
        pass
