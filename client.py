# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~
#
#             MODULE CREATED BY        : ASHUWIN P
#             REVISED & INTEGRATED BY  : ASHUWIN P
#             LAST UPDATE ON           : 26 - DEC - 2023
#
# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students, initially authored by ASHUWIN P and subsequently revised and integrated by the same individual.
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~


import pickle
from validation import (
    ValidationException,
    ClientValidationException,
    OccupantValidationException,
    Validation,
    Validations,
)


class CLIENT_DB:
    """
    Class handling client database operations.
    """

    _file = "client_db.pickle"  # File path for client database

    @staticmethod
    def store_client(data):
        """
        Store client data in the database.

        Args:
        - data: Client object to be stored.

        Returns:
        - None
        """
        try:
            f = open(CLIENT_DB._file, "rb")
            load = pickle.load(f)
            load[data._email_id] = data
            f.close()

            f1 = open(CLIENT_DB._file, "wb")
            pickle.dump(load, f1)
            f1.close()

        except FileNotFoundError:
            dic = {}
            f2 = open(CLIENT_DB._file, "wb")
            dic[data._email_id] = data
            pickle.dump(dic, f2)
            f2.close()

    @staticmethod
    def get_client(email):
        """
        Retrieve client by email.

        Args:
        - email: Email address of the client.

        Returns:
        - Client object or None if not found.
        """
        try:
            f = open(CLIENT_DB._file, "rb")
            DB = pickle.load(f)
            f.close()
            return DB[email]
        except:
            Exception("User Not Found")

    @staticmethod
    def get_all_clients():
        """
        Retrieve all clients from the database.

        Returns:
        - List of all client objects.
        """
        try:
            f = open(CLIENT_DB._file, "rb")
            all_clients = pickle.load(f)
            f.close()
            return list(all_clients.values())
        except FileNotFoundError:
            return []

    @staticmethod
    def show_client(email):
        """
        Display client information by email.

        Args:
        - email: Email address of the client.

        Returns:
        - None
        """
        f = open(CLIENT_DB._file, "rb")
        DB = pickle.load(f)
        f.close()
        return DB[email].display_info()

    @staticmethod
    def show_all_client():
        """
        Display information of all clients in the database.

        Returns:
        - None
        """
        f1 = open(CLIENT_DB._file, "rb")
        load = pickle.load(f1)
        count = 0
        for i, j in load.items():
            print(("-") * 40)
            j.display_info()
            count += 1
        f1.close()

    @staticmethod
    def validate_credential(email, pwd):
        """
        Validate client credentials.

        Args:
        - email: Email address of the client.
        - pwd: Password of the client.

        Returns:
        - bool: True if credentials are valid, False otherwise.
        """
        client = CLIENT_DB.get_client(email)
        if client._password == pwd:
            return True


class Client:
    """
    Class representing a client.
    """

    def __init__(self, name, phone, email, password):
        Validation.Client_Validation(name, phone, email, password)
        self._name = name
        self._phone = phone
        self._email_id = email
        self._password = password
        CLIENT_DB.store_client(self)

    def display_info(self):
        """
        Display client information.

        Returns:
        - None
        """
        print("     Name  : ", self._name)
        print("     Phone : ", self._phone)
        print("     Email : ", self._email_id)


if __name__ == "__main__":
    CLIENT_DB.show_all_client()
