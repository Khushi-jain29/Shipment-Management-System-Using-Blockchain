import hashlib
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class SmartContract:
    def __init__(self, address):
        self.address = address  # Unique address of the smart contract
        self.state = {}  # State of the contract

    def execute(self, transaction):
        """
        Execute transaction logic defined in the smart contract.
        Args:
            transaction (dict): Transaction data.

        Returns:
            bool: True if the transaction is successfully executed, False otherwise.
        """
        # Extract transaction details
        transaction_type = transaction.get("type")
        if transaction_type == "shipment_update":
            return self.update_shipment_status(transaction)
        elif transaction_type == "add_product":
            return self.add_product(transaction)
        else:
            print("Unsupported transaction type:", transaction_type)
            return False

    def update_shipment_status(self, transaction):
        """
        Update the status of a shipment.
        Args:
            transaction (dict): Transaction data containing shipment details.

        Returns:
            bool: True if the shipment status is successfully updated, False otherwise.
        """
        shipment_id = transaction.get("shipment_id")
        new_status = transaction.get("status")
        if shipment_id and new_status:
            self.state[shipment_id] = new_status
            return True
        else:
            print("Invalid shipment update transaction:", transaction)
            return False

    def add_product(self, transaction):
        """
        Add a new product to the system.
        Args:
            transaction (dict): Transaction data containing product details.

        Returns:
            bool: True if the product is successfully added, False otherwise.
        """
        product_id = transaction.get("product_id")
        if product_id:
            self.state[product_id] = transaction
            return True
        else:
            print("Invalid product addition transaction:", transaction)
            return False

# Utility functions for digital signatures
def sign_transaction(private_key, transaction):
    """
    Sign a transaction using a private key.
    Args:
        private_key (object): EC private key.
        transaction (dict): Transaction data.

    Returns:
        bytes: Signature of the transaction.
    """
    serialized_transaction = json.dumps(transaction, sort_keys=True).encode()
    signature = private_key.sign(serialized_transaction, ec.ECDSA(hashes.SHA256()))
    return signature

def verify_signature(public_key, transaction, signature):
    """
    Verify the signature of a transaction using a public key.
    Args:
        public_key (object): EC public key.
        transaction (dict): Transaction data.
        signature (bytes): Signature of the transaction.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    serialized_transaction = json.dumps(transaction, sort_keys=True).encode()
    try:
        public_key.verify(signature, serialized_transaction, ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False


# Sample usage of the SmartContract class with shipment update and product addition

# Initialize the smart contract with a unique address
contract = SmartContract("0x123456789ABCDEF")

# Define a transaction to update the shipment status
shipment_transaction = {
    "type": "shipment_update",
    "shipment_id": "SHIP001",
    "status": "Delivered"
}

# Execute the transaction
update_status = contract.execute(shipment_transaction)
print("Update Shipment Status:", update_status)  # Expected output: True

# Check the updated state of the smart contract
print("Shipment Status in Contract State:", contract.state.get("SHIP001"))  # Expected output: Delivered

# Define a transaction to add a new product
product_transaction = {
    "type": "add_product",
    "product_id": "PRD006",
    "product_name": "New Product",
    "seller_id": "SLR_GuptaE",
    "price": 3000,
    "description": "A new innovative product"
}

# Execute the transaction
add_product = contract.execute(product_transaction)
print("Add Product Status:", add_product)  # Expected output: True

# Check the added product in the contract state
print("Product in Contract State:", contract.state.get("PRD006"))  # Expected output: details of the product transaction
