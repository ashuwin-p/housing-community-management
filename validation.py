# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~
#
#             MODULE CREATED BY        : ARUNKUMAR S
#             REVISED & INTEGRATED BY  : ASHUWIN P
#             LAST UPDATE ON           : 26 - DEC - 2023
#
# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students, created by ARUNKUMAR S and subsequently revised and integrated by ASHUWIN P. 
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

import re
from abc import ABC


class ValidationException(Exception):
    pass


class ClientValidationException(ValidationException):
    pass


class OccupantValidationException(ValidationException):
    pass


class Validation(ABC):
    # Template Method 1
    @staticmethod
    def Client_Validation(ipname, ipnumber, ipemail, ippass):
        """Validate client information.

        Args:
            ipname (str): Name of the client.
            ipnumber (str): Phone number of the client.
            ipemail (str): Email address of the client.
            ippass (str): Password of the client.

        Raises:
            ClientValidationException: If any validation fails.

        Returns:
            bool: True if all validations pass.
        """
        if Validations.validate_name(ipname) is False:
            raise ClientValidationException("Invalid Client Name")
        if Validations.validate_phone(ipnumber) is False:
            raise ClientValidationException("Invalid Client Phone Number")
        if Validations.validate_email(ipemail) is False:
            raise ClientValidationException("Invalid Client Email")
        if Validations.validate_pass(ippass) is False:
            raise ClientValidationException("Invalid Client Password")
        return True

    # Template Method 2
    @staticmethod
    def Occupant_Validation(name, number, aadhar, email, pwd):
        """Validate occupant information.

        Args:
            name (str): Name of the occupant.
            number (str): Phone number of the occupant.
            aadhar (str): Aadhar number of the occupant.
            email (str): Email address of the occupant.
            pwd (str): Password of the occupant.

        Raises:
            OccupantValidationException: If any validation fails.

        Returns:
            bool: True if all validations pass.
        """
        if Validations.validate_name(name) is False:
            raise OccupantValidationException("Invalid Occupant Name")
        if Validations.validate_phone(number) is False:
            raise OccupantValidationException("Invalid Occupant Phone Number")
        if Validations.validate_aadhar(aadhar) is False:
            raise OccupantValidationException("Invalid Occupant Aadhar Number")
        if Validations.validate_pass(pwd) is False:
            raise OccupantValidationException("Invalid Occupant Password")
        if Validations.validate_email(email) is False:
            raise OccupantValidationException("Invalid Occupant Email")
        return True


class Validations:
    # Method to validate name
    @staticmethod
    def validate_name(ipname):
        """Validate a name string.

        Args:
            ipname (str): Name to be validated.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        inpname = "".join((ipname).split())
        if not re.search("^[a-zA-Z][a-zA-Z]*$", inpname):
            return False
        return True

    # Method to validate phone number
    @staticmethod
    def validate_phone(ipnumber):
        """Validate a phone number.

        Args:
            ipnumber (str): Phone number to be validated.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        if not re.search("[0-9]{10}", ipnumber):
            return False
        return True

    # Method to validate Aadhar number
    @staticmethod
    def validate_aadhar(ipnumber):
        """Validate an Aadhar number.

        Args:
            ipnumber (str): Aadhar number to be validated.

        Returns:
            bool: True if the Aadhar number is valid, False otherwise.
        """
        if not re.search("[0-9]{12}", ipnumber):
            return False
        return True

    # Method to validate email
    @staticmethod
    def validate_email(email):
        """Validate an email address.

        Args:
            email (str): Email address to be validated.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[A-Za-z]*\.com$"
        if re.match(pattern, email):
            return True
        return False

    # Method to validate password
    @staticmethod
    def validate_pass(pwd):
        """Validate a password.

        Args:
            pwd (str): Password to be validated.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        # Check if password has at least 8 characters, contains lowercase, uppercase, and digits
        if len(pwd) > 7:
            if not re.search("[a-z]", pwd):
                return False
            if not re.search("[A-Z]", pwd):
                return False
            if not re.search("[0-9]", pwd):
                return False
            return True
        return False
