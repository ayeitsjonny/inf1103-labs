from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: any class that can be shipped must be able
    to work out its own shipping cost. No attributes, no implementation."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost (float)."""
        pass