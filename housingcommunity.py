# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~
#
#             MODULE CREATED BY        : AYUSHMAN NAYAK
#             REVISED & INTEGRATED BY  : ASHUWIN P
#             LAST UPDATE ON           : 26 - DEC - 2023
#
# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~

"""
DISCLAIMER:
    This module represents a collaborative effort undertaken by a group of students, created by AYUSHMAN NAYAK and subsequently revised and integrated by ASHUWIN P. 
    The latest update occurred on December 26, 2023. This code is tailored to fulfill specific functionalities within its designated scope.
    Users are encouraged to review, comprehend, and customize the code to fit their unique project requirements. 
    We strongly advise performing comprehensive testing and validation to ensure compliance with project specifications before deploying it in a live environment.
    Kindly use this code responsibly, adhering to applicable guidelines and best practices. 
    Remember, this project is a part of academic coursework and should be approached in that context.
"""

# ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~


from abc import ABC, abstractmethod
import pickle
from occupant import OCCUPANT_DB


class HC_ERROR(Exception):
    """
    Custom exception class for housing community errors.
    """

    pass


class State(ABC):
    """
    Abstract State class defining the interface for occupancy status.
    """

    state = None

    @abstractmethod
    def change_status(self, flat):
        """
        Abstract method to change occupancy status.

        Args:
        - flat: Flat object to change occupancy status.

        Returns:
        - None
        """
        pass


class UnoccupiedState(State):
    """
    Concrete state representing an unoccupied flat.
    """

    state = "No"

    def change_status(self, flat):
        """
        Change the occupancy status to unoccupied.

        Args:
        - flat: Flat object to change occupancy status.

        Returns:
        - None
        """
        flat._occupancy_status = OccupiedState()
        flat._state = OccupiedState.state


class OccupiedState(State):
    """
    Concrete state representing an occupied flat.
    """

    state = "Yes"

    def change_status(self, flat):
        """
        Change the occupancy status to occupied.

        Args:
        - flat: Flat object to change occupancy status.

        Returns:
        - None
        """
        flat._occupancy_status = UnoccupiedState()
        flat._state = UnoccupiedState.state


class Flat:
    """
    Class representing a flat with occupancy status.
    """

    def __init__(self, block_no, flat_no, bhk):
        self._block_no = block_no
        self._flat_no = flat_no
        self._bhk = bhk
        self._occupant = None
        self._occupancy_status = UnoccupiedState()  # Initial State

    def get_state(self):
        """
        Get the current occupancy state of the flat.

        Returns:
        - str: Current occupancy state ("Yes" for occupied, "No" for unoccupied).
        """
        return self._occupancy_status.state

    def change_occupancy_status(self):
        """
        Change the occupancy status of the flat.

        Returns:
        - None
        """
        self._occupancy_status.change_status(self)

    def occupy(self, occupant):
        """
        Occupy the flat with an occupant.

        Args:
        - occupant: Occupant object to occupy the flat.

        Returns:
        - None

        Raises:
        - HC_ERROR: Raised if already occupied.
        """
        if self.get_state() == "No":
            self.change_occupancy_status()
            occupant._block_no = self._block_no
            occupant._flat_no = self._flat_no
            self._occupant = occupant
            self.update_OC()
            self.update_HC()
        else:
            raise HC_ERROR("Already Occupied !!! ")

    def update_HC(self):
        """
        Update the housing community with flat details.

        Returns:
        - None
        """
        HousingCommunity.GET_HC().update_flat_details(self)

    def update_OC(self):
        """
        Update the occupant database with occupant details.

        Returns:
        - None
        """
        OCCUPANT_DB.store_occupant(self._occupant)


class HousingCommunity:
    """
    Class representing a housing community managing flats and blocks.
    """

    _instance = None

    @staticmethod
    def create_Housing_community():
        """
        Static method to create a Housing Community instance.

        Returns:
        - HousingCommunity instance
        """
        if HousingCommunity._instance is None:
            HousingCommunity._instance = HousingCommunity()
            return HousingCommunity._instance
        else:
            return HousingCommunity._instance

    def __init__(self):
        """
        Constructor method to initialize a HousingCommunity instance.

        Raises:
        - HC_ERROR: Raised if Housing Community is already established.
        """
        if HousingCommunity._instance is None:
            self._blocks = []
            self._flats = {}
            HousingCommunity._instance = self
        else:
            raise HC_ERROR("Housing Community Already Established !")

    @staticmethod
    def GET_HC():
        """
        Static method to retrieve Housing Community from a pickle file.

        Returns:
        - HousingCommunity instance from the pickle file.
        """
        HC_FILE = "housing_community.pickle"
        with open(HC_FILE, "rb") as file:
            return pickle.load(file)

    def Update_HC(self):
        """
        Method to update Housing Community in a pickle file.
        Writes the current instance to the pickle file.

        Returns:
        - None
        """
        HC_FILE = "housing_community.pickle"
        with open(HC_FILE, "wb") as file:
            pickle.dump(self, file)

    def update_flat_details(self, new_flat):
        """
        Update the details of a flat in the housing community.

        Args:
        - new_flat: New Flat object to update in the housing community.

        Returns:
        - None
        """
        block_no = new_flat._block_no
        all_flats = self._flats[block_no]
        for index, flat in enumerate(all_flats):
            if flat._flat_no == new_flat._flat_no:
                self._flats[block_no][index] = new_flat
                self.Update_HC()
                return

    def add_block(self, block):
        """
        Add a block to the housing community.

        Args:
        - block: Block to be added to the housing community.

        Raises:
        - HC_ERROR: Raised if the block already exists.
        """
        block = block.upper()
        if block not in self._blocks:
            self._blocks.append(block)
            self.Update_HC()
        else:
            raise HC_ERROR("Block Already Exists !")

    def add_flat(self, flat):
        """
        Add a flat to the housing community.

        Args:
        - flat: Flat object to be added to the housing community.

        Raises:
        - HC_ERROR: Raised if the block for the flat doesn't exist.
        """
        if flat._block_no in self._blocks:
            if flat._block_no not in self._flats:
                self._flats[flat._block_no] = [flat]
            else:
                self._flats[flat._block_no].append(flat)
            self.Update_HC()
        else:
            raise HC_ERROR("Block Doesn't Exist")

    def list_blocks(self):
        """
        List all the blocks in the housing community.

        Returns:
        - List: List of blocks in the housing community.
        """
        return self._blocks

    def list_flats(self):
        """
        List all the flats in the housing community.

        Returns:
        - List: List of tuples containing block and flat numbers of all flats.
        """
        flats_list = [(block, flat._flat_no) for (block, flat) in self._flats.keys()]
        return flats_list

    def get_unoccupied_flat_objs(self):
        """
        Get a list of unoccupied flat objects in the housing community.

        Returns:
        - List: List of unoccupied flat objects.
        """
        unoccupied_flats = []
        for block_flats in self._flats.values():
            for flat in block_flats:
                if flat._occupancy_status.state == "No":
                    unoccupied_flats.append(flat)
        return unoccupied_flats

    def get_unoccupied_flats_info(self):
        """
        Get information about unoccupied flats in the housing community.

        Returns:
        - List: List of lists containing details of unoccupied flats.
        """
        unoccupied_flats_info = []
        for block_flats in self._flats.values():
            for flat in block_flats:
                if flat._occupancy_status.state == "No":
                    flat_info = [flat._block_no, flat._flat_no, flat._bhk]
                    unoccupied_flats_info.append(flat_info)
        return unoccupied_flats_info

    def get_occupied_flat_objs(self):
        """
        Get a list of occupied flat objects in the housing community.

        Returns:
        - List: List of occupied flat objects.
        """
        occupied_flats = []
        for block_flats in self._flats.values():
            for flat in block_flats:
                if flat._occupancy_status.state == "Yes":
                    occupied_flats.append(flat)
        return occupied_flats

    def list_occupied_flats(self):
        """
        List details of occupied flats in the housing community.

        Returns:
        - List: List of lists containing details of occupied flats.
        """
        occupied_flats = []
        flats = self.get_occupied_flat_objs()
        for block_flats in self._flats.values():
            for flat in block_flats:
                if flat._occupancy_status.state == "Yes":
                    occupied_flats.append(
                        [
                            flat._block_no,
                            flat._flat_no,
                            flat._occupant._name,
                            flat._occupant._phone_no,
                        ]
                    )
        return occupied_flats

    def list_unoccupied_flats(self):
        """
        List details of unoccupied flats in the housing community.

        Returns:
        - List: List of lists containing details of unoccupied flats.
        """
        flats = self.get_unoccupied_flat_objs()
        return [[flat._block_no, flat._flat_no] for flat in flats]

    def get_flat_by_details(self, block_no, flat_no):
        """
        Get flat details by block number and flat number.

        Args:
        - block_no (str): Block number of the flat.
        - flat_no (int): Flat number of the flat.

        Returns:
        - Flat object: Flat object if found, otherwise None.
        """
        flat_no = str(flat_no)
        block_no = block_no.upper()
        if block_no in self._flats:
            all_flats = self._flats[block_no]
            for flat in all_flats:
                if str(flat._flat_no) == flat_no:
                    return flat
        return None


if __name__ == "__main__":
    hc = HousingCommunity.GET_HC()
    # print(hc.list_blocks())
    # print(hc.list_unoccupied_flats())
    # flat = hc.get_flat_by_details("A",101)
    # occupant = OCCUPANT_DB.get_occupant("snehakrishnan@example.com")
    # flat.occupy(occupant)
    # print(hc.list_occupied_flats())
    flat = hc.get_flat_by_details("C", 302)
    print(flat._block_no)
