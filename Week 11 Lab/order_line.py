from product import Product


class OrderLine:
    """
    One product and quantity within an Order.
    Only created by Order (composition). It refers to a Product but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        quantity = int(quantity)
        # Validation: OrderLine owns (and protects) its own quantity rule.
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} "
              f"@ ${self.__product.get_price():.2f} = ${self.calculate_subtotal():.2f}")
        