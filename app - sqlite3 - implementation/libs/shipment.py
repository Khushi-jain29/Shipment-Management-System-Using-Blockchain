class ShipmentManager:
    def __init__(self):
        self.shipments = {}  # Dictionary to store shipment details

    def add_shipment(self, shipment_id, sender, recipient, products):
        """
        Add a new shipment to the system.
        Args:
            shipment_id (str): Unique identifier for the shipment.
            sender (str): Sender's information.
            recipient (str): Recipient's information.
            products (list): List of products included in the shipment.

        Returns:
            bool: True if the shipment is successfully added, False otherwise.
        """
        if shipment_id not in self.shipments:
            self.shipments[shipment_id] = {
                "sender": sender,
                "recipient": recipient,
                "products": products,
                "status": "pending"  # Initial status of the shipment
            }
            return True
        else:
            print("Shipment with ID {} already exists.".format(shipment_id))
            return False

    def update_shipment_status(self, shipment_id, new_status):
        """
        Update the status of a shipment.
        Args:
            shipment_id (str): Unique identifier for the shipment.
            new_status (str): New status of the shipment.

        Returns:
            bool: True if the shipment status is successfully updated, False otherwise.
        """
        if shipment_id in self.shipments:
            self.shipments[shipment_id]["status"] = new_status
            return True
        else:
            print("Shipment with ID {} not found.".format(shipment_id))
            return False

    def get_shipment_status(self, shipment_id):
        """
        Get the current status of a shipment.
        Args:
            shipment_id (str): Unique identifier for the shipment.

        Returns:
            str: Current status of the shipment.
        """
        if shipment_id in self.shipments:
            return self.shipments[shipment_id]["status"]
        else:
            print("Shipment with ID {} not found.".format(shipment_id))
            return None

    def list_shipments(self):
        """
        List all shipments currently in the system.
        Returns:
            dict: Dictionary containing shipment details indexed by shipment IDs.
        """
        return self.shipments
