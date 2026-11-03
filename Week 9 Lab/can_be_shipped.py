from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """
    Interface-style abstract base class.
    Any class that can be shipped must implement calculate_shipping_cost().
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """
        Return the cost of shipping this object.
        """
        pass
