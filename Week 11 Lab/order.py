from order_line import OrderLine
from product import Product
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """
    Composition: an Order creates and owns its OrderLine objects.
    OrderLines are never passed in from outside and never transferred.

    Association: an Order USES one DiscountStrategy. The strategy is passed in,
    is not part of the order, and the same strategy object can be shared by many orders.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """
        Swap the discount strategy at runtime.
        """
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_subtotal(self) -> float:
        """
        Total before any discount.
        """
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    def calculate_total(self) -> float:
        """
        Total after discount. No if/elif on discount types: the strategy decides.
        """
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print("-------------------")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-------------------")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {type(self.__discount).__name__}")
        print(f"Total:    ${self.calculate_total():.2f}")
