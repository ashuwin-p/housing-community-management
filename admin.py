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


class Admin:
    """Singleton Admin class managing admin credentials and authentication."""

    _instance = None
    _file = "admin.pickle"

    def __new__(cls):
        """Create a singleton instance of Admin if it doesn't exist."""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__id = "Admin"
            cls._instance.__password = "123"
            cls._instance.save_to_file()
        return cls._instance

    def save_to_file(self):
        """Save the Admin instance to a pickle file."""
        with open(self._file, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def validate_credential(ipid, ippass):
        """
        Validate admin credentials.

        Args:
        - ipid (str): The admin ID.
        - ippass (str): The admin password.

        Returns:
        - bool: True if credentials are valid, False otherwise.
        """
        try:
            with open(Admin._file, "rb") as file:
                admin_instance = pickle.load(file)
                if ipid == admin_instance.__id and ippass == admin_instance.__password:
                    return True
                return False
        except FileNotFoundError:
            print("Admin pickle file not found.")
            return False


# End of Admin class


# Design Pattern: Singleton pattern is used to ensure only one instance of Admin exists.

if __name__ == "__main__":
    Admin()
    # Validate credentials
    if Admin.validate_credential("Admin", "123"):
        print("Login successful")
    else:
        print("Invalid credentials")
