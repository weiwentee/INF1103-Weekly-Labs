from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """
    Factory pattern: the ONE place that decides which Product subclass to build.
    The rest of the program asks the factory and only works with the Product type.
    Adding a new product type means changing this class (accepted OCP trade-off).
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, extra: float = 0.0) -> Product:
        """
        extra is the subclass-specific value:
          physical -> weight in kg
          digital  -> download size in MB
        """
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
