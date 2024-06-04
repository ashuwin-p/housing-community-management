# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~
#
#             MODULE CREATED BY        : ARUNKUMAR S & BALASUBRAMANIYAM H
#             REVISED & INTEGRATED BY  : ASHUWIN P
#             LAST UPDATE ON           : 26 - DEC - 2023
#
# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~


"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students, created by ARUNKUMAR S & BALASUBRAMANIYAM H and subsequently revised and integrated by ASHUWIN P. 
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

from abc import ABC, abstractmethod
from datetime import datetime


from validation import (
    ValidationException,
    ClientValidationException,
    OccupantValidationException,
    Validation,
    Validations,
)

import pickle

from ps import (
    PaymentStrategy,
    OneBHKPayment,
    TwoBHKPayment,
    ThreeBHKPayment,
)


# State Pattern
class PaymentState(ABC):
    """Abstract class representing Payment State for Occupants."""

    @abstractmethod
    def pay_bill(self, occupant):
        """Abstract method to handle paying bills for occupants."""
        pass

    @abstractmethod
    def check_state_transition(self, occupant):
        """Abstract method to check state transitions for occupants."""
        pass


# PaidState
class PaidState(PaymentState):
    """Class representing the Paid State for Occupants."""

    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def pay_bill(self, occupant):
        """Method to pay bills for occupants in the paid state."""
        self.payment_strategy.pay(occupant)
        occupant.set_payment_state(self)
        occupant.check_state_transition()

    def check_state_transition(self, occupant):
        """Method to check state transitions for occupants in the paid state."""
        current_date = datetime.now()

        # Check if the current date is the first day of the month
        if current_date.day == 1:
            occupant.set_payment_state(UnpaidState(self.payment_strategy))
            # Increment pending_payments by the initial payment amount
            occupant.pending_payments += self.payment_strategy.get_initial_payment()


# Unpaid State
class UnpaidState(PaymentState):
    """Class representing the Unpaid State for Occupants."""

    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def pay_bill(self, occupant):
        """Method to pay bills for occupants in the unpaid state."""
        self.payment_strategy.pay(occupant)
        occupant.set_payment_state(PaidState(self.payment_strategy))
        occupant.check_state_transition()

    def check_state_transition(self, occupant):
        """Method to check state transitions for occupants in the unpaid state."""
        pass


# Observer Pattern
class Observer(ABC):
    """Abstract Observer class."""

    @abstractmethod
    def update(self):
        """Abstract method to update observer."""
        pass


# Observer Pattern
class PaymentObserver(Observer):
    """Observer for Payment status changes."""

    def __init__(self, occupant):
        self.occupant = occupant

    def update(self):
        """Method to update observer on Payment status changes."""
        print(
            f"Payment status changed. Pending Payments: {self.occupant.pending_payments}"
        )


# Payment Database
class PaymentDB:
    """Class to handle Payment Database operations."""

    __file = "payment_db.pickle"

    @staticmethod
    def add_payment(email, payment_amount):
        """Method to add payments to the database."""
        try:
            with open(PaymentDB.__file, "rb") as f:
                payment_data = pickle.load(f)
        except FileNotFoundError:
            payment_data = {}

        if payment_amount > 0:
            payment_data[email] = payment_data.get(email, [])
            payment_data[email].append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": payment_amount,
                }
            )

        with open(PaymentDB.__file, "wb") as f:
            pickle.dump(payment_data, f)

    @staticmethod
    def get_payments():
        """Method to retrieve all payments."""
        try:
            with open(PaymentDB.__file, "rb") as f:
                payment_data = pickle.load(f)
                nested_rows = []
                for email, payments in payment_data.items():
                    for payment in payments:
                        nested_rows.append([email, payment["amount"], payment["date"]])
                return nested_rows
        except FileNotFoundError:
            return []

    @staticmethod
    def get_payment_history(email):
        """Method to retrieve payment history by email."""
        try:
            with open(PaymentDB.__file, "rb") as f:
                payment_data = pickle.load(f)
            return payment_data.get(email, [])
        except FileNotFoundError:
            return []


# Class to handle occupant database operations
class OCCUPANT_DB:
    # File path for occupant database
    _file = "occupant_db.pickle"

    # Method to store occupant data in the database
    @staticmethod
    def store_occupant(data):
        """Stores occupant data in the database.

        Args:
            data: Occupant data to be stored.
        """
        try:
            # Load existing database
            f = open(OCCUPANT_DB._file, "rb")
            load = pickle.load(f)
            load[data._email_id] = data
            f.close()

            # Update database with new data
            f1 = open(OCCUPANT_DB._file, "wb")
            pickle.dump(load, f1)
            f1.close()

        except FileNotFoundError:
            # Create a new database if it doesn't exist
            dic = {}
            f2 = open(OCCUPANT_DB._file, "wb")
            dic[data._email_id] = data
            pickle.dump(dic, f2)
            f2.close()

    # Method to display occupant information by email
    @staticmethod
    def show_occupant(email):
        """Displays occupant information by email.

        Args:
            email: Email of the occupant.

        Returns:
            Information of the occupant corresponding to the email.
        """
        f = open(OCCUPANT_DB._file, "rb")
        DB = pickle.load(f)
        f.close()
        return DB[email].dispaly_info()

    # Method to get occupant by email
    @staticmethod
    def get_occupant(email):
        """Gets an occupant by email.

        Args:
            email: Email of the occupant.

        Returns:
            Occupant corresponding to the email.
        """
        f = open(OCCUPANT_DB._file, "rb")
        DB = pickle.load(f)
        f.close()
        return DB[email]

    # Method to display information of all occupants in the database
    @staticmethod
    def show_all_occupant():
        """Displays information of all occupants in the database."""
        f1 = open(OCCUPANT_DB._file, "rb")
        load = pickle.load(f1)
        count = 0
        for i, j in load.items():
            print(("*") * 40)
            j.dispaly_info()
            count += 1
        f1.close()

    # Method to remove occupant by email
    @staticmethod
    def remove_occupant(email):
        """Removes an occupant by email.

        Args:
            email: Email of the occupant to be removed.

        Returns:
            Removed occupant.
        """
        f4 = open(OCCUPANT_DB._file, "rb")
        load = pickle.load(f4)
        remove = load.pop(email, None)
        # Update
        f5 = open(OCCUPANT_DB._file, "wb")
        pickle.dump(load, f5)
        f5.close()
        return remove

    @staticmethod
    def validate_credential(email, pwd):
        """Validates occupant's credentials.

        Args:
            email: Email of the occupant.
            pwd: Password to be validated.

        Returns:
            True if credentials are valid, otherwise False.
        """
        occupant = OCCUPANT_DB.get_occupant(email)
        if occupant._password == pwd:
            return True


# Class representing an occupant
class OCCUPANT:
    # Constructor to initialize occupant attributes and validate them
    def __init__(
        self,
        NAME,
        PHONE_NO,
        AADHAR_NO,
        EMAIL_ID,
        PASSWORD,
        BLOCK_NO,
        FLAT_NO,
        payment_strategy,
    ):
        """Initialize an occupant object with attributes and payment strategy.

        Args:
            NAME (str): Name of the occupant.
            PHONE_NO (str): Phone number of the occupant.
            AADHAR_NO (str): Aadhar number of the occupant.
            EMAIL_ID (str): Email ID of the occupant.
            PASSWORD (str): Password of the occupant.
            BLOCK_NO (str): Block number of the occupant's flat.
            FLAT_NO (int): Flat number of the occupant.
            payment_strategy (PaymentState): Payment strategy for the occupant.
        """
        # Validate occupant attributes
        Validation.Occupant_Validation(NAME, PHONE_NO, AADHAR_NO, EMAIL_ID, PASSWORD)
        # Assign attributes
        self._name = NAME
        self._phone_no = PHONE_NO
        self._aadhar_no = AADHAR_NO
        self._email_id = EMAIL_ID
        self._password = PASSWORD
        self._flat_no = FLAT_NO
        self._block_no = BLOCK_NO

        # PAYMENT
        self.payment_strategy = payment_strategy
        self.pending_payments = self.payment_strategy.get_initial_payment()
        self.payment_state = UnpaidState(self.payment_strategy)
        self.observers = []
        self.last_payment_date = datetime.now()

        # Store occupant data in the database
        OCCUPANT_DB.store_occupant(self)

    def get_amount(self):
        """Get the pending payment amount.

        Returns:
            int: Pending payment amount.
        """
        return self.pending_payments

    def pay_bill(self):
        """Process payment of the occupant's bill."""
        amount = self.get_amount()
        self.payment_state.pay_bill(self)
        PaymentDB.add_payment(self._email_id, amount)
        self.pending_payments = 0
        self.notify_observers()
        OCCUPANT_DB.store_occupant(self)
        return True

    def set_payment_state(self, state):
        """Set the payment state for the occupant.

        Args:
            state (PaymentState): Payment state to be set.
        """
        self.payment_state = state

    def notify_observers(self):
        """Notify all observers."""
        for observer in self.observers:
            observer.update()

    def check_state_transition(self):
        """Check the state transition for the occupant."""
        self.payment_state.check_state_transition(self)

    def vacate_flat(self):
        """Vacate the flat by removing occupant from the database."""
        if self._pending_payments == 0:
            OCCUPANT_DB.remove_occupant(self._email_id)
        else:
            raise Exception("Pay the pending Amount !")

    def dispaly_info(self):
        """Display occupant information."""
        print("NAME         :", self._name)
        print("PHONE NUMBER :", self._phone_no)
        print("AADHAR NO    :", self._aadhar_no)
        print("EMAIL ID     :", self._email_id)
        print("FLAT NO      :", self._flat_no)
        print("BLOCK NO     :", self._block_no)
        print("PENDING PAY  :", self._pending_payment)
