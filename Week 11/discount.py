from __future__ import annotations

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: one task (discounting an order total) that can be
    done in several ways. Each way lives in its own class, and they all
    share this one method, so Order can call apply() without knowing which
    discount it has. A new discount = a new subclass; Order never changes
    (Open/Closed Principle)."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after this discount."""
        pass


class NoDiscount(DiscountStrategy):
    """Default strategy: leaves the total unchanged. Using a 'do nothing'
    object means Order never has to check for None."""

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    """Takes a fixed percentage off, e.g. PercentageDiscount(10) = 10% off."""

    def __init__(self, percent: float):
        if (isinstance(percent, bool) or not isinstance(percent, (int, float))
                or not 0 < percent <= 100):
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percent: float = float(percent)

    def get_percent(self) -> float:
        return self.__percent

    def apply(self, total: float) -> float:
        return total * (1 - self.__percent / 100)

    def __str__(self) -> str:
        return f"{self.__percent:g}% off"


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) = $20 off orders of $200 or more."""

    def __init__(self, threshold: float, amount: float):
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) \
                or threshold < 0:
            raise ValueError("Threshold must be a number >= 0.")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) \
                or amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)  # never a negative total
        return total

    def __str__(self) -> str:
        return f"${self.__amount:g} off orders of ${self.__threshold:g}+"


class StudentDiscount(DiscountStrategy):
    """Section 2.4 - added WITHOUT touching Order: 5% off for students."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)

    def __str__(self) -> str:
        return "Student discount (5% off)"
