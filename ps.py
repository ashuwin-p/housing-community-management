# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~
#
#             MODULE CREATED BY        : BALASUBRAMANIYAM H
#             REVISED & INTEGRATED BY  : ASHUWIN P
#             LAST UPDATE ON           : 26 - DEC - 2023
#
# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~


"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students, created by BALASUBRAMANIYAM H and subsequently revised and integrated by ASHUWIN P. 
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

from abc import ABC, abstractmethod


# Strategy Pattern
class PaymentStrategy(ABC):
    @abstractmethod
    def get_initial_payment(self):
        """Get the initial payment amount.

        Returns:
            int: The initial payment amount.
        """
        pass

    @abstractmethod
    def pay(self, occupant):
        """Make a payment based on the strategy.

        Args:
            occupant: The occupant to make the payment.
        """
        pass


# Concrete Strategy: 1 BHK Payment
class OneBHKPayment(PaymentStrategy):
    def get_initial_payment(self):
        """Get the initial payment for a 1 BHK flat.

        Returns:
            int: The initial payment for a 1 BHK flat.
        """
        return 500

    def pay(self, occupant):
        """Make a payment for a 1 BHK flat.

        Args:
            occupant: The occupant making the payment.
        """
        occupant.pending_payments += self.get_initial_payment()


# Concrete Strategy: 2 BHK Payment
class TwoBHKPayment(PaymentStrategy):
    def get_initial_payment(self):
        """Get the initial payment for a 2 BHK flat.

        Returns:
            int: The initial payment for a 2 BHK flat.
        """
        return 700

    def pay(self, occupant):
        """Make a payment for a 2 BHK flat.

        Args:
            occupant: The occupant making the payment.
        """
        occupant.pending_payments += self.get_initial_payment()


# Concrete Strategy: 3 BHK Payment
class ThreeBHKPayment(PaymentStrategy):
    def get_initial_payment(self):
        """Get the initial payment for a 3 BHK flat.

        Returns:
            int: The initial payment for a 3 BHK flat.
        """
        return 900

    def pay(self, occupant):
        """Make a payment for a 3 BHK flat.

        Args:
            occupant: The occupant making the payment.
        """
        occupant.pending_payments += self.get_initial_payment()
