class Database:
    def __init__(self):
        self.shipments = {}  # Dictionary to store shipment data
        self.transactions = []  # List to store transaction data
        self.smart_contracts = {}  # Dictionary to store smart contract data

    def save_shipment(self, shipment_id, shipment_data):
        """
        Save shipment data to the database.
        Args:
            shipment_id (str): Unique identifier for the shipment.
            shipment_data (dict): Data associated with the shipment.

        Returns:
            bool: True if the shipment data is successfully saved, False otherwise.
        """
        if shipment_id not in self.shipments:
            self.shipments[shipment_id] = shipment_data
            return True
        else:
            print("Shipment with ID {} already exists.".format(shipment_id))
            return False

    def get_shipment(self, shipment_id):
        """
        Retrieve shipment data from the database.
        Args:
            shipment_id (str): Unique identifier for the shipment.

        Returns:
            dict: Data associated with the shipment.
        """
        return self.shipments.get(shipment_id)

    def save_transaction(self, transaction):
        """
        Save transaction data to the database.
        Args:
            transaction (dict): Transaction data.

        Returns:
            bool: True if the transaction data is successfully saved, False otherwise.
        """
        self.transactions.append(transaction)
        return True

    def save_smart_contract(self, contract_address, contract_data):
        """
        Save smart contract data to the database.
        Args:
            contract_address (str): Address of the smart contract.
            contract_data (dict): Data associated with the smart contract.

        Returns:
            bool: True if the smart contract data is successfully saved, False otherwise.
        """
        if contract_address not in self.smart_contracts:
            self.smart_contracts[contract_address] = contract_data
            return True
        else:
            print("Smart contract with address {} already exists.".format(contract_address))
            return False

    def get_smart_contract(self, contract_address):
        """
        Retrieve smart contract data from the database.
        Args:
            contract_address (str): Address of the smart contract.

        Returns:
            dict: Data associated with the smart contract.
        """
        return self.smart_contracts.get(contract_address)
