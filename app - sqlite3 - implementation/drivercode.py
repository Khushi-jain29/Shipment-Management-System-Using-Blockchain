from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import sqlite3
import datetime
import hashlib
from db_utils import *
from email_sender import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to manage session data

#-------------------Customer Routes--------------------------------

# Utility function to get database connection
def get_db_connection():
    conn = sqlite3.connect('db_design/shipment_management_system.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Customer Login
@app.route('/ShipmentManagementSystem/Customer/Login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        user_id = request.form.get('UserID')
        password = request.form.get('Password')

        print(f"Received POST: UserID={user_id}, Password={password}")

        if user_id and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE UserID = ? AND Password = ? AND UserType = 'Consumer'", (user_id, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['logged_in_user_id'] = user_id
                session['logged_in_user_role'] = 'Consumer'
                session['logged_in_user_email'] = user['Email']

                print(f"Login Successful: UserID={user_id}")

                send_email(user['Email'],
                           'LogisticsCo - Shipment Tracking and Management System - Login Alert',
                           'Hey User, You are logged into LogisticsCo App as Customer')
                return redirect(url_for('customer_landing'))
        
        flash('Invalid Credentials. Please try again.')
        return redirect(url_for('customer_login'))

    return render_template("user_login.html")

# Customer Landing Page
@app.route('/ShipmentManagementSystem/Customer/Home')
def customer_landing():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return redirect(url_for('customer_login'))
    return render_template("user_landing.html")

# Track Shipment
@app.route('/ShipmentManagementSystem/Customer/TrackShipment', methods=['GET'])
def customer_track_shipment():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401

    tracking_number = request.args.get('trackingNumber')
    print(tracking_number)
    if not tracking_number:
        return jsonify({"error": "Tracking number is required"}), 400

    # Open database connection
    with get_db_connection() as conn:
        db_cursor = conn.cursor()
        # Fetch shipment history based on the tracking number, ordered by TimeStamp
        db_cursor.execute("SELECT * FROM ShipmentHistory WHERE TrackingID = ? ORDER BY TimeStamp ASC", (tracking_number,))
        history_list = db_cursor.fetchall()

    if not history_list:
        return jsonify({"error": "No tracking details created for this shipment."}), 404

    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate', 
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions', 
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID']
    history_list = [dict(zip(columns, row)) for row in history_list]

    # Validate the shipment through the blockchain
    is_valid, validation_message, validated_records = validate_shipment(tracking_number)

    # Append validation status to each record
    for record in validated_records:
        record['ShipmentValidation'] = record.get('ValidationStatus', 'Unknown')

    print(validated_records)
    return jsonify(validated_records)

def validate_shipment(tracking_number):
    """Validate the shipment's blockchain record and return the validation status."""
    with get_db_connection() as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT * FROM ShipmentHistory WHERE TrackingID = ? ORDER BY TimeStamp ASC", (tracking_number,))
        records = db_cursor.fetchall()

    if not records:
        return False, "Validation Failed: No records found.", []

    # Convert database rows to dictionaries
    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate',
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions',
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID']
    records = [dict(zip(columns, row)) for row in records]

    # Perform blockchain validation
    is_valid, validation_message = verify_chain(records)

    return is_valid, validation_message, records

def create_hash(*args):
    """Hashes the input provided using SHA-256."""
    hashing_text = "".join(map(str, args))
    return hashlib.sha256(hashing_text.encode('utf-8')).hexdigest()

def verify_chain(records):
    """Verifies the integrity of the blockchain by checking hashes block by block."""
    previous_hash = ""
    all_valid = True
    failed_record_id = None

    for idx, record in enumerate(records):
        # Handle the first block separately since it has no computed previous hash
        if idx == 0:
            record_data = (
                f"{record['PreviousHash']}"  # Use stored PreviousHash for the first block
                f"{record['ShipmentID']}"
                f"{record['StatusUpdate']}"
                f"{record['CurrentLocation']}"
                f"{record['TimeStamp']}"
                f"{record['Weight']}"
                f"{record['Dimensions']}"
            )
            current_hash = create_hash(record_data)

            if record['RecordHash'] != current_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid RecordHash'
            else:
                record['ValidationStatus'] = 'Valid'
        else:
            # Use the computed previous hash for subsequent blocks
            record_data = (
                f"{previous_hash}"  # Use computed previous hash
                f"{record['ShipmentID']}"
                f"{record['StatusUpdate']}"
                f"{record['CurrentLocation']}"
                f"{record['TimeStamp']}"
                f"{record['Weight']}"
                f"{record['Dimensions']}"
            )
            current_hash = create_hash(record_data)

            # Validate RecordHash
            if record['RecordHash'] != current_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid RecordHash'
            # Validate chain linkage
            elif record['PreviousHash'] != previous_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid PreviousHash'
            else:
                record['ValidationStatus'] = 'Valid'

        # Update previous_hash for next iteration
        previous_hash = record['RecordHash']

        # If a failure is detected, continue to validate remaining blocks but note the failure
        if not all_valid and failed_record_id == record['HistoryID']:
            # Mark subsequent blocks as invalid due to previous chain break
            for remaining_record in records[idx+1:]:
                remaining_record['ValidationStatus'] = 'Invalid due to previous error'
            break  # Stop processing further since the chain is broken

    if all_valid:
        return True, "Validated"
    else:
        return False, f"Validation failed at record with HistoryID: {failed_record_id}"

# Order History
@app.route('/ShipmentManagementSystem/Customer/OrderHistory', methods=['GET'])
def user_order_history():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401

    logged_in_user_id = session['logged_in_user_id']

    with get_db_connection() as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT * FROM Shipments WHERE CustomerID = ?", (logged_in_user_id,))
        shipments_list = db_cursor.fetchall()

    columns = ['ShipmentID', 'TrackingID', 'OrderRefNo', 'ProductID', 'CustomerID', 
               'InitialStatus', 'EstimatedDeliveryDate', 'Origin', 'Destination', 
               'Weight', 'Dimensions']
    shipments_list = [dict(zip(columns, row)) for row in shipments_list]
    return jsonify(shipments_list)

# View Products
@app.route('/ShipmentManagementSystem/Customer/ViewProducts', methods=['GET'])
def customer_view_products():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()

    columns = ['ProductID', 'SellerID', 'ProductName', 'ProductDescription', 'Price', 
               'Brand', 'Category', 'ModelName', 'ShipsFrom', 'SoldBy', 
               'WarrantyPolicy', 'ProductImageUrl', 'AdditionalFeatures']
    products_list = [dict(zip(columns, product)) for product in products]
    return jsonify(products_list)

# View Product Details
@app.route('/ShipmentManagementSystem/Customer/ViewProduct', methods=['GET'])
def customer_view_product():
    product_id = request.args.get('ProductID')
    if not product_id:
        return jsonify({"error": "ProductID is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE ProductID = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    columns = ['ProductID', 'SellerID', 'ProductName', 'ProductDescription', 'Price', 
               'Brand', 'Category', 'ModelName', 'ShipsFrom', 'SoldBy', 
               'WarrantyPolicy', 'ProductImageUrl', 'AdditionalFeatures']
    product_dict = dict(zip(columns, product))
    return jsonify(product_dict)

# Notifications
@app.route('/ShipmentManagementSystem/Customer/Notifications', methods=['GET'])
def customer_notifications():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['logged_in_user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Notifications WHERE UserID = ? ORDER BY TimeStamp DESC", (user_id,))
    notifications = cursor.fetchall()
    conn.close()

    columns = ['NotificationID', 'UserID', 'Message', 'TimeStamp']
    notifications_list = [dict(zip(columns, notification)) for notification in notifications]
    return jsonify(notifications_list)

# Profile
@app.route('/ShipmentManagementSystem/Customer/Profile', methods=['GET'])
def customer_profile():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['logged_in_user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, UserName, Email, ContactNum FROM Users WHERE UserID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    columns = ['UserID', 'UserName', 'Email', 'ContactNum']
    user_dict = dict(zip(columns, user))
    return jsonify(user_dict)

# Update Password
@app.route('/ShipmentManagementSystem/Customer/UpdatePassword', methods=['POST'])
def customer_update_password():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    new_password = data.get('newPassword')
    confirm_password = data.get('confirmPassword')
    
    if not new_password or not confirm_password:
        return jsonify({"message": "Both new password and confirmation are required."}), 400
    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match."}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Password = ? WHERE UserID = ?", (new_password, session['logged_in_user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Password updated successfully."}), 200

# Support - Submit Support Ticket
@app.route('/ShipmentManagementSystem/Customer/Support', methods=['POST'])
def customer_support():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Consumer':
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')
    
    if not subject or not message:
        return jsonify({"message": "Subject and message are required."}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO SupportTickets (UserID, Subject, Message, TimeStamp)
                      VALUES (?, ?, ?, ?)""",
                   (session['logged_in_user_id'], subject, message, datetime.datetime.utcnow()))
    conn.commit()
    conn.close()

    send_email('support@logisticsco.in', 
               'New Support Ticket', 
               f"User {session['logged_in_user_id']} submitted a support ticket.\nSubject: {subject}\nMessage: {message}")
    
    return jsonify({"message": "Support ticket submitted successfully."}), 201

# Logout
@app.route('/ShipmentManagementSystem/Logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home_page'))

#---------------------Other Routes---------------------

@app.route('/ShipmentManagementSystem/home')
def home_page():
    return render_template("home.html")

@app.route('/ShipmentManagementSystem/Register')
def user_register():
    return render_template("all_user_register.html")


#-------------------Seller Routes--------------------------------

# Seller Login
@app.route('/ShipmentManagementSystem/Seller/Login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        user_id = request.form.get('UserID')
        password = request.form.get('Password')

        if user_id and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE UserID = ? AND Password = ? AND UserType = 'Seller'", (user_id, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['logged_in_user_id'] = user_id
                session['logged_in_user_role'] = 'Seller'
                session['logged_in_user_email'] = user['Email']

                send_email(user['Email'],
                           'LogisticsCo - Shipment Tracking and Management System - Login Alert',
                           'Hey Seller, You are logged into LogisticsCo App as Seller')
                return redirect(url_for('seller_landing'))
        
        flash('Invalid Credentials. Please try again.')
        return redirect(url_for('seller_login'))

    return render_template("seller_login.html")

# Seller Landing Page
@app.route('/ShipmentManagementSystem/Seller/Home')
def seller_landing():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return redirect(url_for('seller_login'))
    return render_template("seller_landing.html")

# Product Management
@app.route('/ShipmentManagementSystem/Seller/Products', methods=['GET', 'POST', 'PUT', 'DELETE'])
def seller_products():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    seller_id = session['logged_in_user_id']

    if request.method == 'GET':
        product_id = request.args.get('ProductID')
        conn = get_db_connection()
        cursor = conn.cursor()
        if product_id:
            # Fetch specific product
            cursor.execute("SELECT * FROM Products WHERE SellerID = ? AND ProductID = ?", (seller_id, product_id))
            product = cursor.fetchone()
            conn.close()
            if not product:
                return jsonify({"error": "Product not found."}), 404
            columns = ['ProductID', 'SellerID', 'ProductName', 'ProductDescription', 'Price',
                       'Brand', 'Category', 'ModelName', 'ShipsFrom', 'SoldBy',
                       'WarrantyPolicy', 'ProductImageUrl', 'AdditionalFeatures']
            product_dict = dict(zip(columns, product))
            return jsonify(product_dict)
        else:
            # View all products
            cursor.execute("SELECT * FROM Products WHERE SellerID = ?", (seller_id,))
            products = cursor.fetchall()
            conn.close()
            columns = ['ProductID', 'SellerID', 'ProductName', 'ProductDescription', 'Price',
                       'Brand', 'Category', 'ModelName', 'ShipsFrom', 'SoldBy',
                       'WarrantyPolicy', 'ProductImageUrl', 'AdditionalFeatures']
            products_list = [dict(zip(columns, product)) for product in products]
            return jsonify(products_list)

    elif request.method == 'POST':
        # Add New Product
        data = request.get_json()
        product_id = data.get('ProductID')
        product_name = data.get('ProductName')
        product_description = data.get('ProductDescription')
        price = data.get('Price')
        brand = data.get('Brand')
        category = data.get('Category')
        model_name = data.get('ModelName')
        ships_from = data.get('ShipsFrom')
        sold_by = data.get('SoldBy')
        warranty_policy = data.get('WarrantyPolicy')
        product_image_url = data.get('ProductImageUrl')
        additional_features = data.get('AdditionalFeatures')

        if not product_id or not product_name or not price:
            return jsonify({"message": "ProductID, ProductName, and Price are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Products (ProductID, SellerID, ProductName, ProductDescription, Price,
                              Brand, Category, ModelName, ShipsFrom, SoldBy, WarrantyPolicy, ProductImageUrl, AdditionalFeatures)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (product_id, seller_id, product_name, product_description, price,
                            brand, category, model_name, ships_from, sold_by,
                            warranty_policy, product_image_url, additional_features))
            conn.commit()
            return jsonify({"message": "Product added successfully."}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({"message": f"Error adding product: {str(e)}"}), 400
        finally:
            conn.close()

    elif request.method == 'PUT':
        # Update Product
        data = request.get_json()
        product_id = data.get('ProductID')
        if not product_id:
            return jsonify({"message": "ProductID is required for updating a product."}), 400

        # Update fields
        update_fields = {k: v for k, v in data.items() if v is not None and k != 'ProductID'}
        if not update_fields:
            return jsonify({"message": "No fields provided for update."}), 400

        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values())
        values.append(product_id)
        values.append(seller_id)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Products SET {set_clause} WHERE ProductID = ? AND SellerID = ?", values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Product updated successfully."}), 200

    elif request.method == 'DELETE':
        # Delete Product
        product_id = request.args.get('ProductID')
        if not product_id:
            return jsonify({"message": "ProductID is required for deleting a product."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE ProductID = ? AND SellerID = ?", (product_id, seller_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Product deleted successfully."}), 200

# Order Management
@app.route('/ShipmentManagementSystem/Seller/Orders', methods=['GET'])
def seller_orders():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    seller_id = session['logged_in_user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.* 
        FROM Shipments s
        INNER JOIN Products p ON s.ProductID = p.ProductID
        WHERE p.SellerID = ?
    """, (seller_id,))
    orders = cursor.fetchall()
    conn.close()

    columns = ['ShipmentID', 'TrackingID', 'OrderRefNo', 'ProductID', 'CustomerID',
               'InitialStatus', 'EstimatedDeliveryDate', 'Origin', 'Destination',
               'Weight', 'Dimensions']
    orders_list = [dict(zip(columns, order)) for order in orders]
    return jsonify(orders_list)

# Initiate Shipment
@app.route('/ShipmentManagementSystem/Seller/InitiateShipment', methods=['POST'])
def seller_initiate_shipment():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    shipment_id = data.get('ShipmentID')
    tracking_id = data.get('TrackingID')
    order_ref_no = data.get('OrderRefNo')
    product_id = data.get('ProductID')
    customer_id = data.get('CustomerID')
    initial_status = data.get('InitialStatus', 'Order Created')
    estimated_delivery_date = data.get('EstimatedDeliveryDate', (datetime.datetime.utcnow() + datetime.timedelta(days=5)).date())
    origin = data.get('Origin')
    destination = data.get('Destination')
    weight = data.get('Weight')
    dimensions = data.get('Dimensions')

    if not shipment_id or not tracking_id or not order_ref_no or not product_id or not customer_id:
        return jsonify({"message": "ShipmentID, TrackingID, OrderRefNo, ProductID, and CustomerID are required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO Shipments (ShipmentID, TrackingID, OrderRefNo, ProductID, CustomerID,
                          InitialStatus, EstimatedDeliveryDate, Origin, Destination, Weight, Dimensions)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (shipment_id, tracking_id, order_ref_no, product_id, customer_id,
                        initial_status, estimated_delivery_date, origin, destination, weight, dimensions))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({"message": f"Error initiating shipment: {str(e)}"}), 400
    finally:
        conn.close()

    # Create initial shipment history with blockchain record
    history_id = hashlib.sha256((shipment_id + tracking_id + datetime.datetime.utcnow().isoformat()).encode('utf-8')).hexdigest()
    status_update = initial_status
    current_location = origin
    timestamp = datetime.datetime.utcnow().isoformat()
    carrier_name = 'LogisticsCo'
    comments = ''
    previous_hash = 'None'
    record_data = f"{previous_hash}{shipment_id}{status_update}{current_location}{timestamp}{weight}{dimensions}"
    record_hash = create_hash(record_data)
    block_id = hashlib.sha256(record_hash.encode('utf-8')).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO ShipmentHistory (HistoryID, ShipmentID, TrackingID, OrderRefNo, StatusUpdate,
                      CurrentLocation, TimeStamp, CarrierName, Weight, Dimensions, Comments,
                      PreviousHash, RecordHash, BlockID)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (history_id, shipment_id, tracking_id, order_ref_no, status_update,
                    current_location, timestamp, carrier_name, weight, dimensions, comments,
                    previous_hash, record_hash, block_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Shipment initiated successfully."}), 201

# View Shipment Status
@app.route('/ShipmentManagementSystem/Seller/ShipmentStatus', methods=['GET'])
def seller_shipment_status():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    tracking_id = request.args.get('TrackingID')
    if not tracking_id:
        return jsonify({"error": "TrackingID is required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShipmentHistory WHERE TrackingID = ? ORDER BY TimeStamp ASC", (tracking_id,))
    shipment_history = cursor.fetchall()
    conn.close()

    if not shipment_history:
        return jsonify({"error": "No shipment history found for this TrackingID."}), 404

    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate',
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions',
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID']
    history_list = [dict(zip(columns, record)) for record in shipment_history]

    # Validate the shipment through the blockchain
    is_valid, validation_message, validated_records = validate_shipment(tracking_id)

    # Append validation status to each record
    for record in validated_records:
        record['ShipmentValidation'] = record.get('ValidationStatus', 'Unknown')

    return jsonify(validated_records)

# Execute Smart Contracts (Basic Implementation)
@app.route('/ShipmentManagementSystem/Seller/SmartContracts', methods=['GET'])
def seller_smart_contracts():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    # For demonstration, we'll return a list of smart contracts
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SmartContracts")
    contracts = cursor.fetchall()
    conn.close()

    columns = ['ContractID', 'ContractName', 'Description', 'Code', 'TriggerEvent', 'CreatedAt', 'CreatedBy']
    contracts_list = [dict(zip(columns, contract)) for contract in contracts]
    return jsonify(contracts_list)

# Profile Management
@app.route('/ShipmentManagementSystem/Seller/Profile', methods=['GET', 'POST'])
def seller_profile():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Seller':
        return jsonify({"error": "Unauthorized"}), 401

    seller_id = session['logged_in_user_id']

    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, UserName, Email, ContactNum FROM Users WHERE UserID = ?", (seller_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        columns = ['UserID', 'UserName', 'Email', 'ContactNum']
        user_dict = dict(zip(columns, user))
        return jsonify(user_dict)

    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('Email')
        contact_num = data.get('ContactNum')

        if not email and not contact_num:
            return jsonify({"message": "At least one field (Email or ContactNum) must be provided to update."}), 400

        update_fields = {}
        if email:
            update_fields['Email'] = email
        if contact_num:
            update_fields['ContactNum'] = contact_num

        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values())
        values.append(seller_id)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Users SET {set_clause} WHERE UserID = ?", values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Profile updated successfully."}), 200
#-------------------Logistics Routes-------------------
# Logistics Login
@app.route('/ShipmentManagementSystem/Logistics/Login', methods=['GET', 'POST'])
def logistics_login():
    if request.method == 'POST':
        user_id = request.form.get('UserID')
        password = request.form.get('Password')
        print(user_id)
        if user_id and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE UserID = ? AND Password = ? AND UserType = 'Logistics'", (user_id, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['logged_in_user_id'] = user_id
                session['logged_in_user_role'] = 'Logistics'
                session['logged_in_user_email'] = user['Email']

                flash('Logged in successfully as Logistics personnel.')
                return redirect(url_for('logistics_landing'))

        flash('Invalid Credentials. Please try again.')
        return redirect(url_for('logistics_login'))

    return render_template("logistics_login.html")

# Logistics Landing Page
@app.route('/ShipmentManagementSystem/Logistics/Home')
def logistics_landing():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return redirect(url_for('logistics_login'))
    return render_template("logistics_landing.html")

# Real-Time Shipment Monitoring and Tracking
@app.route('/ShipmentManagementSystem/Logistics/Shipments', methods=['GET'])
def logistics_shipments():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*, sh.StatusUpdate, sh.CurrentLocation, sh.TimeStamp
        FROM Shipments s
        LEFT JOIN (
            SELECT sh1.*
            FROM ShipmentHistory sh1
            INNER JOIN (
                SELECT TrackingID, MAX(TimeStamp) as MaxTimeStamp
                FROM ShipmentHistory
                GROUP BY TrackingID
            ) sh2 ON sh1.TrackingID = sh2.TrackingID AND sh1.TimeStamp = sh2.MaxTimeStamp
        ) sh ON s.TrackingID = sh.TrackingID
    """)
    shipments = cursor.fetchall()
    conn.close()

    columns = ['ShipmentID', 'TrackingID', 'OrderRefNo', 'ProductID', 'CustomerID',
               'InitialStatus', 'EstimatedDeliveryDate', 'Origin', 'Destination',
               'Weight', 'Dimensions', 'StatusUpdate', 'CurrentLocation', 'TimeStamp']
    shipments_list = [dict(zip(columns, shipment)) for shipment in shipments]
    return jsonify(shipments_list)

# Blockchain Integrity Validation for Shipments
@app.route('/ShipmentManagementSystem/Logistics/ValidateShipment', methods=['GET'])
def logistics_validate_shipment():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return jsonify({"error": "Unauthorized"}), 401

    tracking_id = request.args.get('TrackingID')
    if not tracking_id:
        return jsonify({"error": "TrackingID is required"}), 400

    # Perform validation
    is_valid, validation_message, validated_records = validate_shipment(tracking_id)

    # Return the validation result
    return jsonify({
        "is_valid": is_valid,
        "validation_message": validation_message,
        "validated_records": validated_records
    })

# Update Shipment Status and Automated Alerts
@app.route('/ShipmentManagementSystem/Logistics/UpdateShipmentStatus', methods=['POST'])
def logistics_update_shipment_status():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    shipment_id = data.get('ShipmentID')
    tracking_id = data.get('TrackingID')
    status_update = data.get('StatusUpdate')
    current_location = data.get('CurrentLocation')
    weight = data.get('Weight')
    dimensions = data.get('Dimensions')
    comments = data.get('Comments', '')

    if not shipment_id or not tracking_id or not status_update or not current_location:
        return jsonify({"message": "ShipmentID, TrackingID, StatusUpdate, and CurrentLocation are required."}), 400

    # Fetch the latest ShipmentHistory for PreviousHash
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RecordHash FROM ShipmentHistory 
        WHERE TrackingID = ? ORDER BY TimeStamp DESC LIMIT 1
    """, (tracking_id,))
    last_record = cursor.fetchone()
    previous_hash = last_record['RecordHash'] if last_record else 'None'

    timestamp = datetime.datetime.utcnow().isoformat()
    record_data = f"{previous_hash}{shipment_id}{status_update}{current_location}{timestamp}{weight}{dimensions}"
    record_hash = create_hash(record_data)
    block_id = hashlib.sha256(record_hash.encode('utf-8')).hexdigest()
    history_id = hashlib.sha256((shipment_id + tracking_id + timestamp).encode('utf-8')).hexdigest()

    # Insert new ShipmentHistory record
    cursor.execute("""INSERT INTO ShipmentHistory (HistoryID, ShipmentID, TrackingID, OrderRefNo, StatusUpdate,
                      CurrentLocation, TimeStamp, CarrierName, Weight, Dimensions, Comments,
                      PreviousHash, RecordHash, BlockID, CreatedBy)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (history_id, shipment_id, tracking_id, '', status_update,
                    current_location, timestamp, 'LogisticsCo', weight, dimensions, comments,
                    previous_hash, record_hash, block_id, session['logged_in_user_id']))
    conn.commit()

    # Check for critical events and create notifications
    critical_events = ['Delayed', 'Cancelled', 'Exception']
    if status_update in critical_events:
        # Insert notification for logistics personnel
        notification_message = f"Shipment {shipment_id} has a critical update: {status_update}."
        cursor.execute("""INSERT INTO Notifications (UserID, Message, TimeStamp)
                          VALUES (?, ?, ?)""",
                       (session['logged_in_user_id'], notification_message, timestamp))
        # Insert notification for customer
        cursor.execute("SELECT CustomerID FROM Shipments WHERE ShipmentID = ?", (shipment_id,))
        customer = cursor.fetchone()
        if customer:
            customer_id = customer['CustomerID']
            cursor.execute("""INSERT INTO Notifications (UserID, Message, TimeStamp)
                              VALUES (?, ?, ?)""",
                           (customer_id, notification_message, timestamp))
        conn.commit()
    conn.close()

    return jsonify({"message": "Shipment status updated successfully."}), 201

# Shipment History Viewer
@app.route('/ShipmentManagementSystem/Logistics/ShipmentHistory', methods=['GET'])
def logistics_shipment_history():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return jsonify({"error": "Unauthorized"}), 401

    tracking_id = request.args.get('TrackingID')
    if not tracking_id:
        return jsonify({"error": "TrackingID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShipmentHistory WHERE TrackingID = ? ORDER BY TimeStamp ASC", (tracking_id,))
    shipment_history = cursor.fetchall()
    conn.close()

    if not shipment_history:
        return jsonify({"error": "No shipment history found for this TrackingID."}), 404

    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate',
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions',
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID', 'CreatedBy', 'VerifiedBy', 'ChangeLog']
    history_list = [dict(zip(columns, record)) for record in shipment_history]

    # Optionally, include blockchain validation status
    is_valid, validation_message, validated_records = validate_shipment(tracking_id)
    for record in validated_records:
        record['ShipmentValidation'] = record.get('ValidationStatus', 'Unknown')

    return jsonify(validated_records)

# Digital Proof of Delivery (PoD) via Smart Contracts
@app.route('/ShipmentManagementSystem/Logistics/ConfirmDelivery', methods=['POST'])
def logistics_confirm_delivery():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Logistics':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    shipment_id = data.get('ShipmentID')
    tracking_id = data.get('TrackingID')
    current_location = data.get('CurrentLocation')
    recipient_name = data.get('RecipientName')
    recipient_signature = data.get('RecipientSignature')  # This could be an encoded string representing the signature

    if not shipment_id or not tracking_id or not current_location or not recipient_name or not recipient_signature:
        return jsonify({"message": "All fields are required for confirming delivery."}), 400

    # Fetch the latest ShipmentHistory for PreviousHash
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RecordHash FROM ShipmentHistory 
        WHERE TrackingID = ? ORDER BY TimeStamp DESC LIMIT 1
    """, (tracking_id,))
    last_record = cursor.fetchone()
    previous_hash = last_record['RecordHash'] if last_record else 'None'

    status_update = 'Delivered'
    timestamp = datetime.datetime.utcnow().isoformat()
    weight = None
    dimensions = None
    comments = f"Recipient: {recipient_name}, Signature: {recipient_signature}"
    record_data = f"{previous_hash}{shipment_id}{status_update}{current_location}{timestamp}{weight}{dimensions}"
    record_hash = create_hash(record_data)
    block_id = hashlib.sha256(record_hash.encode('utf-8')).hexdigest()
    history_id = hashlib.sha256((shipment_id + tracking_id + timestamp).encode('utf-8')).hexdigest()

    # Insert new ShipmentHistory record
    cursor.execute("""INSERT INTO ShipmentHistory (HistoryID, ShipmentID, TrackingID, OrderRefNo, StatusUpdate,
                      CurrentLocation, TimeStamp, CarrierName, Weight, Dimensions, Comments,
                      PreviousHash, RecordHash, BlockID, CreatedBy)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (history_id, shipment_id, tracking_id, '', status_update,
                    current_location, timestamp, 'LogisticsCo', weight, dimensions, comments,
                    previous_hash, record_hash, block_id, session['logged_in_user_id']))
    conn.commit()

    # Store the digital PoD in the blockchain (simulated via ShipmentHistory)
    # Notify customer about delivery
    cursor.execute("SELECT CustomerID FROM Shipments WHERE ShipmentID = ?", (shipment_id,))
    customer = cursor.fetchone()
    if customer:
        customer_id = customer['CustomerID']
        notification_message = f"Your shipment {shipment_id} has been delivered. Thank you!"
        cursor.execute("""INSERT INTO Notifications (UserID, Message, TimeStamp)
                          VALUES (?, ?, ?)""",
                       (customer_id, notification_message, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Delivery confirmed and PoD generated successfully."}), 201

#-------------------Admin Routes (Placeholder)-------------------

# Function to verify the blockchain chain
def verify_chain_admin(records):
    previous_hash = ""
    all_valid = True
    failed_record_id = None

    for idx, record in enumerate(records):
        # Handle the first block separately since it has no computed previous hash
        if idx == 0:
            record_data = (
                f"{record['PreviousHash']}"  # Use stored PreviousHash for the first block
                f"{record['ShipmentID']}"
                f"{record['StatusUpdate']}"
                f"{record['CurrentLocation']}"
                f"{record['TimeStamp']}"
                f"{record['Weight']}"
                f"{record['Dimensions']}"
            )
            current_hash = create_hash(record_data)

            if record['RecordHash'] != current_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid RecordHash'
            else:
                record['ValidationStatus'] = 'Valid'
        else:
            # Use the computed previous hash for subsequent blocks
            record_data = (
                f"{previous_hash}"  # Use computed previous hash
                f"{record['ShipmentID']}"
                f"{record['StatusUpdate']}"
                f"{record['CurrentLocation']}"
                f"{record['TimeStamp']}"
                f"{record['Weight']}"
                f"{record['Dimensions']}"
            )
            current_hash = create_hash(record_data)

            # Validate RecordHash
            if record['RecordHash'] != current_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid RecordHash'
            # Validate chain linkage
            elif record['PreviousHash'] != previous_hash:
                all_valid = False
                failed_record_id = record['HistoryID']
                record['ValidationStatus'] = 'Invalid PreviousHash'
            else:
                record['ValidationStatus'] = 'Valid'

        # Update previous_hash for next iteration
        previous_hash = record['RecordHash']

        # If a failure is detected, continue to validate remaining blocks but note the failure
        if not all_valid and failed_record_id == record['HistoryID']:
            # Mark subsequent blocks as invalid due to previous chain break
            for remaining_record in records[idx+1:]:
                remaining_record['ValidationStatus'] = 'Invalid due to previous error'
            break  # Stop processing further since the chain is broken

    if all_valid:
        return True, "Blockchain is valid."
    else:
        return False, f"Blockchain validation failed at record with HistoryID: {failed_record_id}"

# Admin Login
@app.route('/ShipmentManagementSystem/Admin/Login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_id = request.form.get('UserID')
        password = request.form.get('Password')

        if user_id and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE UserID = ? AND Password = ? AND UserType = 'Administrator'", (user_id, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['logged_in_user_id'] = user_id
                session['logged_in_user_role'] = 'Administrator'
                session['logged_in_user_email'] = user['Email']

                flash('Logged in successfully as Administrator.')
                return redirect(url_for('admin_landing'))

        flash('Invalid Credentials. Please try again.')
        return redirect(url_for('admin_login'))

    return render_template("admin_login.html")

# Admin Landing Page
@app.route('/ShipmentManagementSystem/Admin/Home')
def admin_landing():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return redirect(url_for('admin_login'))
    return render_template("admin_landing.html")

# Comprehensive Smart Contract Management
@app.route('/ShipmentManagementSystem/Admin/SmartContracts', methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin_smart_contracts():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SmartContracts")
        contracts = cursor.fetchall()
        conn.close()

        columns = ['ContractID', 'ContractName', 'Description', 'Code', 'TriggerEvent', 'CreatedAt', 'CreatedBy']
        contracts_list = [dict(zip(columns, contract)) for contract in contracts]
        return jsonify(contracts_list)

    elif request.method == 'POST':
        data = request.get_json()
        contract_id = data.get('ContractID')
        contract_name = data.get('ContractName')
        description = data.get('Description')
        code = data.get('Code')
        trigger_event = data.get('TriggerEvent')
        created_by = session['logged_in_user_id']

        if not contract_id or not contract_name or not code or not trigger_event:
            return jsonify({"message": "ContractID, ContractName, Code, and TriggerEvent are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO SmartContracts (ContractID, ContractName, Description, Code, TriggerEvent, CreatedAt, CreatedBy)
                              VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (contract_id, contract_name, description, code, trigger_event, datetime.datetime.utcnow(), created_by))
            conn.commit()
        except sqlite3.IntegrityError as e:
            return jsonify({"message": f"Error creating smart contract: {str(e)}"}), 400
        finally:
            conn.close()

        return jsonify({"message": "Smart contract created successfully."}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        contract_id = data.get('ContractID')
        update_fields = {k: v for k, v in data.items() if k != 'ContractID' and v is not None}

        if not contract_id or not update_fields:
            return jsonify({"message": "ContractID and at least one field to update are required."}), 400

        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values())
        values.append(contract_id)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE SmartContracts SET {set_clause} WHERE ContractID = ?", values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Smart contract updated successfully."}), 200

    elif request.method == 'DELETE':
        contract_id = request.args.get('ContractID')
        if not contract_id:
            return jsonify({"message": "ContractID is required for deleting a smart contract."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SmartContracts WHERE ContractID = ?", (contract_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Smart contract deleted successfully."}), 200

# Blockchain Metadata Analysis and Audit
@app.route('/ShipmentManagementSystem/Admin/BlockchainAudit', methods=['GET'])
def admin_blockchain_audit():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BlockchainMetadata ORDER BY CreatedAt DESC")
    metadata = cursor.fetchall()
    conn.close()

    columns = ['MetadataID', 'LastBlockHash', 'CreatedAt']
    metadata_list = [dict(zip(columns, data)) for data in metadata]
    return jsonify(metadata_list)

# Validate Entire Blockchain for Consistency
@app.route('/ShipmentManagementSystem/Admin/ValidateBlockchain', methods=['GET'])
def admin_validate_blockchain():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    # Fetch all shipment history records to validate the entire blockchain
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShipmentHistory ORDER BY TimeStamp ASC")
    records = cursor.fetchall()
    conn.close()

    # Convert database rows to dictionaries
    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate',
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions',
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID']
    records = [dict(zip(columns, row)) for row in records]

    # Perform blockchain validation
    is_valid, validation_message = verify_chain_admin(records)

    return jsonify({
        "is_valid": is_valid,
        "validation_message": validation_message,
        "validated_records": records
    })

# Admin - Read All Tables Data
@app.route('/ShipmentManagementSystem/Admin/AllData', methods=['GET'])
def admin_all_data():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    tables = ['Users', 'Products', 'Shipments', 'ShipmentHistory', 'SmartContracts', 'BlockchainMetadata', 'Approvals', 'Roles', 'Permissions', 'RolePermissions', 'UserRoles', 'SupportTickets', 'Notifications']
    all_data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data_list = [dict(zip(columns, row)) for row in rows]
        all_data[table] = data_list

    conn.close()
    return jsonify(all_data)

# Admin - Get All Tracking IDs
@app.route('/ShipmentManagementSystem/Admin/GetAllTrackingIDs', methods=['GET'])
def admin_get_all_tracking_ids():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT TrackingID FROM Shipments")
    tracking_ids = [row['TrackingID'] for row in cursor.fetchall()]
    conn.close()

    return jsonify(tracking_ids)

# Admin - Get Validation Data for Tracking ID
@app.route('/ShipmentManagementSystem/Admin/GetValidationData', methods=['GET'])
def admin_get_validation_data():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    tracking_id = request.args.get('TrackingID')
    if not tracking_id:
        return jsonify({"error": "TrackingID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShipmentHistory WHERE TrackingID = ? ORDER BY TimeStamp ASC", (tracking_id,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        return jsonify({"error": "No shipment history found for this TrackingID."}), 404

    # Convert database rows to dictionaries
    columns = ['HistoryID', 'ShipmentID', 'TrackingID', 'OrderRefNo', 'StatusUpdate',
               'CurrentLocation', 'TimeStamp', 'CarrierName', 'Weight', 'Dimensions',
               'Comments', 'PreviousHash', 'RecordHash', 'BlockID']
    records = [dict(zip(columns, row)) for row in records]

    # Perform blockchain validation
    is_valid, validation_message = verify_chain_admin(records)

    return jsonify({
        "is_valid": is_valid,
        "validation_message": validation_message,
        "validated_records": records
    })

# Admin - Halt Shipment
@app.route('/ShipmentManagementSystem/Admin/HaltShipment', methods=['POST'])
def admin_halt_shipment():
    if 'logged_in_user_id' not in session or session.get('logged_in_user_role') != 'Administrator':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    shipment_id = data.get('ShipmentID')
    if not shipment_id:
        return jsonify({"message": "ShipmentID is required to halt a shipment."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    # Update the shipment's status to 'Halted'
    cursor.execute("UPDATE Shipments SET InitialStatus = 'Halted' WHERE ShipmentID = ?", (shipment_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Shipment {shipment_id} has been halted successfully."}), 200


#------------------------------------------------------------------------
if __name__ == '__main__':
    port = 7000
    print("To access application, go to:", "http://127.0.0.1:" + str(port) + "/ShipmentManagementSystem/home\n\n\n")
    app.run(host="localhost", port=port, debug=True)
