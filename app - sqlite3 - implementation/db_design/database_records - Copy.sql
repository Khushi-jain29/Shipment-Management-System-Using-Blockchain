-- Inserting Companies
INSERT INTO Companies (CompanyName, Description) VALUES 
    ('Agarwal Fabrics', 'Leading fabric supplier with a wide range of textiles.'),
    ('Pune Handlooms', 'Specializes in traditional handloom products.'),
    ('Gupta Electronics', 'Retailer of electronic gadgets and appliances.'),
    ('Patel Organic Store', 'Offers a variety of organic and natural products.'),
    ('Hyderabad Jewellers', 'Premium jewelry store with exclusive designs.'),
    ('LogisticsCo', 'Global logistics and transportation services.'),
    ('SmartTech Solutions', 'Provider of smart home and office solutions.'),
    ('FashionHub', 'Trendy and affordable fashion apparel.'),
    ('HomeEssentials', 'Essential items for home and living.'),
    ('TechGear', 'Latest gadgets and tech accessories.'),
    ('TechWorld', 'Supplier of cutting-edge technology products.'),
    ('EcoHome', 'Eco-friendly home products and solutions.');

-- Inserting Users

-- Consumers
INSERT INTO Users (UserID, UserName, UserType, Password, Email, ContactNum, RegistrationDate) 
VALUES 
    ('CNS_RajeshK', 'Rajesh Kumar', 'Consumer', 'rajesh123', 'rajesh.kumar@email.com', '9876543210', '2023-01-01'),
    ('CNS_SunitaG', 'Sunita Gupta', 'Consumer', 'sunita456', 'sunita.gupta@email.com', '9876543211', '2023-01-01'),
    ('CNS_AmitS', 'Amit Singh', 'Consumer', 'amit789', 'amit.singh@email.com', '9876543212', '2023-01-01'),
    ('CNS_PriyaS', 'Priya Sharma', 'Consumer', 'priya101', 'priya.sharma@email.com', '9876543213', '2023-01-01'),
    ('CNS_VikramR', 'Vikram Reddy', 'Consumer', 'vikram202', 'vikram.reddy@email.com', '9876543214', '2023-01-01'),
    ('CNS_SamiraT', 'Samira Thomas', 'Consumer', 'samira321', 'samira.thomas@email.com', '9876543215', '2023-01-05'),
    ('CNS_RohanB', 'Rohan Bhattacharya', 'Consumer', 'rohan654', 'rohan.bhattacharya@email.com', '9876543216', '2023-01-05');

-- Sellers
INSERT INTO Users (UserID, UserName, UserType, Password, Email, ContactNum, RegistrationDate) 
VALUES 
    ('SLR_AgarwalF', 'Agarwal Fabrics', 'Seller', 'agarwal123', 'contact@agarwalfabrics.in', '9848012345', '2023-01-02'),
    ('SLR_PuneH', 'Pune Handlooms', 'Seller', 'pune456', 'sales@punehandlooms.in', '9822012345', '2023-01-02'),
    ('SLR_GuptaE', 'Gupta Electronics', 'Seller', 'gupta789', 'info@guptaelectronics.in', '9810012345', '2023-01-02'),
    ('SLR_PatelO', 'Patel Organic Store', 'Seller', 'patel101', 'support@patelorganic.in', '9898012345', '2023-01-02'),
    ('SLR_HydJ', 'Hyderabad Jewellers', 'Seller', 'hyd202', 'inquiry@hydjewellers.in', '9866012345', '2023-01-02'),
    ('SLR_TechWorld', 'TechWorld', 'Seller', 'techworld123', 'sales@techworld.com', '9876543217', '2023-01-06');

-- Logistics
INSERT INTO Users (UserID, UserName, UserType, Password, Email, ContactNum, RegistrationDate) 
VALUES 
    ('LOG_AaravM', 'Aarav Logistics Manager', 'Logistics', 'logistics1', 'aarav.manager@logisticsco.in', '9201234567', '2023-01-03'),
    ('LOG_MeeraD', 'Meera Dispatch Supervisor', 'Logistics', 'logistics2', 'meera.supervisor@logisticsco.in', '9301234567', '2023-01-03'),
    ('LOG_RohanF', 'Rohan Fleet Coordinator', 'Logistics', 'logistics3', 'rohan.coordinator@logisticsco.in', '9401234567', '2023-01-03'),
    ('LOG_IshaO', 'Isha Operations Analyst', 'Logistics', 'logistics4', 'isha.analyst@logisticsco.in', '9501234567', '2023-01-03'),
    ('LOG_VikasR', 'Vikas Route Planner', 'Logistics', 'logistics5', 'vikas.planner@logisticsco.in', '9601234567', '2023-01-03');

-- Administrators
INSERT INTO Users (UserID, UserName, UserType, Password, Email, ContactNum, RegistrationDate) 
VALUES 
    ('ADM_AditiS', 'Aditi System Admin', 'Administrator', 'adminpass1', 'aditi.admin@logisticsco.in', '8801234567', '2023-01-04'),
    ('ADM_NitinD', 'Nitin Database Manager', 'Administrator', 'adminpass2', 'nitin.manager@logisticsco.in', '8811234567', '2023-01-04'),
    ('ADM_KiranIT', 'Kiran IT Support', 'Administrator', 'adminpass3', 'kiran.support@logisticsco.in', '8821234567', '2023-01-04'),
    ('ADM_AnjaliN', 'Anjali Network Admin', 'Administrator', 'adminpass4', 'anjali.netadmin@logisticsco.in', '8831234567', '2023-01-04'),
    ('ADM_SureshD', 'Suresh Data Analyst', 'Administrator', 'adminpass5', 'suresh.analyst@logisticsco.in', '8841234567', '2023-01-04');

-- Inserting Roles
INSERT INTO Roles (RoleName) VALUES 
    ('Consumer'),
    ('Seller'),
    ('Logistics Manager'),
    ('Logistics Supervisor'),
    ('Logistics Coordinator'),
    ('Logistics Analyst'),
    ('Administrator');

-- Inserting Permissions
INSERT INTO Permissions (PermissionName) VALUES 
    ('View Shipments'),
    ('Update Shipments'),
    ('Create Shipments'),
    ('Delete Shipments'),
    ('View Users'),
    ('Update Users'),
    ('Create Users'),
    ('Delete Users'),
    ('Manage Roles'),
    ('Manage Permissions'),
    ('Access Reports'),
    ('Configure System'),
    ('View Products'),
    ('Update Products'),
    ('Create Products'),
    ('Delete Products'),
    ('Manage Contracts'),
    ('Approve Transactions'),
    ('View Blockchain'),
    ('Access Smart Contracts');

-- Inserting RolePermissions

-- Consumer
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (1, 1), -- View Shipments
    (1, 5), -- View Users (limited)
    (1, 13); -- View Products

-- Seller
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (2, 13), -- View Products
    (2, 14), -- Update Products
    (2, 15), -- Create Products
    (2, 16); -- Delete Products

-- Logistics Manager
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (3, 1), -- View Shipments
    (3, 2), -- Update Shipments
    (3, 3), -- Create Shipments
    (3, 4); -- Delete Shipments

-- Logistics Supervisor
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (4, 1), -- View Shipments
    (4, 2); -- Update Shipments

-- Logistics Coordinator
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (5, 1), -- View Shipments
    (5, 3); -- Create Shipments

-- Logistics Analyst
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (6, 11), -- Access Reports
    (6, 19); -- View Blockchain

-- Administrator
INSERT INTO RolePermissions (RoleID, PermissionID) VALUES 
    (7, 5), -- View Users
    (7, 6), -- Update Users
    (7, 7), -- Create Users
    (7, 8), -- Delete Users
    (7, 9), -- Manage Roles
    (7, 10), -- Manage Permissions
    (7, 12), -- Configure System
    (7, 17), -- Manage Contracts
    (7, 18); -- Approve Transactions

-- Inserting UserRoles

-- Consumers (Each has the 'Consumer' role)
INSERT INTO UserRoles (UserID, RoleID) VALUES 
    ('CNS_RajeshK', 1),
    ('CNS_SunitaG', 1),
    ('CNS_AmitS', 1),
    ('CNS_PriyaS', 1),
    ('CNS_VikramR', 1),
    ('CNS_SamiraT', 1),
    ('CNS_RohanB', 1);

-- Sellers (Each has the 'Seller' role)
INSERT INTO UserRoles (UserID, RoleID) VALUES 
    ('SLR_AgarwalF', 2),
    ('SLR_PuneH', 2),
    ('SLR_GuptaE', 2),
    ('SLR_PatelO', 2),
    ('SLR_HydJ', 2),
    ('SLR_TechWorld', 2);

-- Logistics (Each has specific logistics roles)
INSERT INTO UserRoles (UserID, RoleID) VALUES 
    ('LOG_AaravM', 3), -- Logistics Manager
    ('LOG_MeeraD', 4), -- Logistics Supervisor
    ('LOG_RohanF', 5), -- Logistics Coordinator
    ('LOG_IshaO', 6), -- Logistics Analyst
    ('LOG_VikasR', 6); -- Logistics Analyst

-- Administrators (Each has the 'Administrator' role)
INSERT INTO UserRoles (UserID, RoleID) VALUES 
    ('ADM_AditiS', 7),
    ('ADM_NitinD', 7),
    ('ADM_KiranIT', 7),
    ('ADM_AnjaliN', 7),
    ('ADM_SureshD', 7);

-- Inserting Products
INSERT INTO Products (ProductID, SellerID, ProductName, ProductDescription, Price, Brand, Category, ModelName, ShipsFrom, SoldBy, WarrantyPolicy, ProductImageUrl, AdditionalFeatures)
VALUES 
    ('PRD001', 'SLR_GuptaE', 'Samsung 27-inch M5 Smart Monitor', 'FHD Smart Monitor with Speakers, Remote, 1 Billion Color, Smart TV apps, and more', 24999, 'Samsung', 'Electronics', 'LS27BM501EWXXL', 'Samsung Warehouse', 'Samsung', '2-Year Warranty', 'http://imageurl.com/samsungmonitor', 'Smart TV apps, Apple Airplay, Dex'),
    ('PRD002', 'SLR_GuptaE', 'Logitech MK215 Wireless Keyboard and Mouse Combo', '2.4 GHz Wireless, Compact Design, Long Battery Life', 1299, 'Logitech', 'Computer Accessories', 'MK215', 'Logitech Warehouse', 'Logitech', '3-Year Warranty', 'http://imageurl.com/logitechcombo', '2-Year Keyboard Battery Life, 5-Month Mouse Battery Life'),
    ('PRD003', 'SLR_GuptaE', 'Google Nest WiFi', '4x4 AC2200 Wi-Fi Mesh System with 4400 Sq ft Coverage', 15999, 'Google', 'Electronics', 'Nest WiFi Router 2-Pack', 'Google Warehouse', 'Google', '1-Year Warranty', 'http://imageurl.com/googlenestwifi', 'Router 2-Pack, Mesh System'),
    ('PRD004', 'SLR_HydJ', 'Malabar Gold 18K Yellow Gold Chain', 'BIS Hallmark (750) 18K Yellow Gold Chain for Women', 50000, 'Malabar Gold & Diamonds', 'Jewelry', '18KYGChain', 'Malabar Store', 'Malabar Gold & Diamonds', 'Lifetime Warranty', 'http://imageurl.com/malabargoldchain', 'BIS Hallmark'),
    ('PRD005', 'SLR_GuptaE', 'Sony Alpha ILCE-7M3 Digital SLR Camera', 'Full-Frame 24.2MP Mirrorless Camera, 4K, Real-Time Eye Auto Focus', 175000, 'Sony', 'Electronics', 'Alpha ILCE-7M3', 'Sony Warehouse', 'Sony', '2-Year Warranty', 'http://imageurl.com/sonyalpha', '4K Vlogging, Tiltable LCD'),
    ('PRD006', 'SLR_AgarwalF', 'Premium Silk Saree', 'Handcrafted premium silk saree with intricate designs', 15000, 'Agarwal Fabrics', 'Apparel', 'SilkSaree001', 'Agarwal Warehouse', 'Agarwal Fabrics', '1-Year Warranty', 'http://imageurl.com/silksaree', 'Handwoven, Colorfast'),
    ('PRD007', 'SLR_PuneH', 'Traditional Handloom Tablecloth', 'Elegant handloom tablecloth perfect for dining', 2500, 'Pune Handlooms', 'Home Decor', 'TableclothT001', 'Pune Warehouse', 'Pune Handlooms', '6-Month Warranty', 'http://imageurl.com/tablecloth', 'Machine Washable'),
    ('PRD008', 'SLR_PatelO', 'Organic Honey', 'Pure organic honey sourced from natural farms', 800, 'Patel Organic', 'Food', 'HoneyPure001', 'Patel Organic Warehouse', 'Patel Organic Store', 'No Warranty', 'http://imageurl.com/organichoney', 'Raw, Unfiltered'),
    ('PRD009', 'SLR_HydJ', 'Diamond Stud Earrings', 'Elegant diamond stud earrings for all occasions', 120000, 'Hyderabad Jewellers', 'Jewelry', 'DiamondStud001', 'HydJ Warehouse', 'Hyderabad Jewellers', 'Lifetime Warranty', 'http://imageurl.com/diamondstud', 'Conflict-Free Diamonds'),
    ('PRD010', 'SLR_TechWorld', 'Smart LED Bulb', 'Wi-Fi enabled LED bulb with color changing capabilities', 999, 'TechWorld', 'Electronics', 'SmartLED001', 'TechWorld Warehouse', 'TechWorld', '1-Year Warranty', 'http://imageurl.com/smartled', 'Voice Control, Energy Efficient'),
    ('PRD011', 'SLR_PuneH', 'Handloom Cushion Covers', 'Set of 4 handcrafted handloom cushion covers with traditional patterns', 3500, 'Pune Handlooms', 'Home Decor', 'CushionC001', 'Pune Warehouse', 'Pune Handlooms', '6-Month Warranty', 'http://imageurl.com/cushioncovers', 'Machine Washable, Durable'),
    ('PRD012', 'SLR_PatelO', 'Organic Skincare Set', 'Complete organic skincare set including cleanser, toner, and moisturizer', 4500, 'Patel Organic', 'Beauty', 'SkincareSet001', 'Patel Organic Warehouse', 'Patel Organic Store', 'No Warranty', 'http://imageurl.com/skincareset', 'Natural Ingredients, Paraben-Free'),
    ('PRD013', 'SLR_HydJ', 'Gold Plated Necklace', 'Elegant gold-plated necklace with gemstone accents', 75000, 'Hyderabad Jewellers', 'Jewelry', 'GoldNecklace001', 'HydJ Warehouse', 'Hyderabad Jewellers', 'Lifetime Warranty', 'http://imageurl.com/goldnecklace', 'Gemstone Accents, Hypoallergenic'),
    ('PRD014', 'SLR_TechWorld', 'Wireless Earbuds', 'Bluetooth 5.0 wireless earbuds with noise cancellation', 2999, 'TechWorld', 'Electronics', 'Earbuds001', 'TechWorld Warehouse', 'TechGear', '1-Year Warranty', 'http://imageurl.com/wirelessearbuds', 'Noise Cancellation, Touch Controls'),
    ('PRD015', 'SLR_AgarwalF', 'Cotton Bed Sheets', 'Set of 2 premium cotton bed sheets with floral patterns', 4000, 'Agarwal Fabrics', 'Apparel', 'BedSheets001', 'Agarwal Warehouse', 'Agarwal Fabrics', '1-Year Warranty', 'http://imageurl.com/bedsheets', 'Breathable, Soft Fabric');

-- Inserting Shipments
INSERT INTO Shipments (ShipmentID, TrackingID, OrderRefNo, ProductID, CustomerID, InitialStatus, EstimatedDeliveryDate, Origin, Destination, Weight, Dimensions)
VALUES 
    ('SHIP001', 'TRACK340274928915', 'ORD40597892194758711', 'PRD001', 'CNS_RajeshK', 'Order Created', '2024-04-05', 'Samsung Warehouse', 'Mumbai, IN', 5.5, '50x30x10 cm'),
    ('SHIP002', 'TRACK340324923129', 'ORD40588547834026720', 'PRD002', 'CNS_RajeshK', 'Order Created', '2023-04-03', 'Logitech Warehouse', 'Kolkata, IN', 2.0, '40x20x5 cm'),
    ('SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'PRD003', 'CNS_SamiraT', 'Order Created', '2024-05-10', 'Google Warehouse', 'Delhi, IN', 3.2, '30x15x5 cm'),
    ('SHIP004', 'TRACK340274928917', 'ORD40597892194758713', 'PRD004', 'CNS_AmitS', 'Order Created', '2024-06-15', 'Malabar Store', 'Bangalore, IN', 1.5, '20x10x5 cm'),
    ('SHIP005', 'TRACK340274928918', 'ORD40597892194758714', 'PRD005', 'CNS_PriyaS', 'Order Created', '2024-07-20', 'Sony Warehouse', 'Chennai, IN', 4.0, '45x25x15 cm'),
    ('SHIP006', 'TRACK340274928919', 'ORD40597892194758715', 'PRD006', 'CNS_VikramR', 'Order Created', '2024-08-25', 'Agarwal Warehouse', 'Hyderabad, IN', 2.5, '35x20x10 cm'),
    ('SHIP007', 'TRACK340274928920', 'ORD40597892194758716', 'PRD007', 'CNS_RajeshK', 'Order Created', '2024-09-30', 'Pune Warehouse', 'Ahmedabad, IN', 1.0, '25x15x5 cm'),
    ('SHIP008', 'TRACK340274928921', 'ORD40597892194758717', 'PRD008', 'CNS_SamiraT', 'Order Created', '2024-10-05', 'Patel Organic Warehouse', 'Jaipur, IN', 6.0, '60x40x20 cm'),
    ('SHIP009', 'TRACK340274928922', 'ORD40597892194758718', 'PRD009', 'CNS_AmitS', 'Order Created', '2024-11-10', 'HydJ Warehouse', 'Lucknow, IN', 3.5, '40x25x10 cm'),
    ('SHIP010', 'TRACK340274928923', 'ORD40597892194758719', 'PRD010', 'CNS_PriyaS', 'Order Created', '2024-12-15', 'TechWorld Warehouse', 'Pune, IN', 5.0, '50x30x15 cm');

-- Inserting ShipmentHistory Records


INSERT INTO ShipmentHistory (HistoryID, ShipmentID, TrackingID, OrderRefNo, StatusUpdate,
                             CurrentLocation, TimeStamp, CarrierName, Weight, Dimensions,
                             Comments, PreviousHash, RecordHash, BlockID)
VALUES 
    ('b12ebadcf5533e05b444e55051ad4662b78dd1882643e5a8bbdafa8425dd15fb', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Carrier picked up the package', 'Delhi, IN',
     '2024-03-29 06:30:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', 'None', 'a91ce977bfd1bea7713210f62742b64990d8b99a28b227c5e3b49fae45da57ff', 'da158036db078946214bf58f58acc7cb675a84c2da97ae360a51c11fc9f18c1f'),

    ('1f669614b2eed08cb550f2e9f83348ad2903767bf8bc122606366e66d5157a81', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package has left the origin facility', 'Delhi, IN',
     '2024-03-29 08:00:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', 'a91ce977bfd1bea7713210f62742b64990d8b99a28b227c5e3b49fae45da57ff', '7de72fd1501dfdf2c9c0f475dcaaeb0b82f5fa40419de4dabbb811229a4773b4', 'f7b4fcfb7704bc36ed4dabbf066e22999deb75868137a8a9f2f392cc0f53b776'),

    ('169ef5c68bd2f5a874bb2242a2bf6dc802867149554d25d5f2d21d700b2dfeda', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package arrived at an interim facility', 'Indore, IN',
     '2024-03-31 14:35:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', '7de72fd1501dfdf2c9c0f475dcaaeb0b82f5fa40419de4dabbb811229a4773b4', 'caaf6ec76a1796c2c6712aa00f4759ec432dacf067455f33ae7858cab47e0108', '141340e1d957ef2dc1b21fc44d5250c9ad33855f279f2879d7ed6a32a24ed207'),

    ('ce29e82595e2c12c1f503f976e2b056031a9f8bbfa5c4a7b29c7dcbb0934411f', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package has left an interim facility', 'Indore, IN',
     '2024-04-01 18:15:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', 'caaf6ec76a1796c2c6712aa00f4759ec432dacf067455f33ae7858cab47e0108', '84e79756bcde13053713177333fb92f88897ca11155b91a9013449901eb56798', '38f10ddc82e3c24bf4e3c0d2f46666f1128395c414963f01918ebecc59406a3f'),

    ('456d8215187413c6c4f0c380b878427f283b93d45edf2f2be3d6971156c45942', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package arrived at an interim facility', 'Pune, IN',
     '2024-04-02 23:26:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', '84e79756bcde13053713177333fb92f88897ca11155b91a9013449901eb56798', '8f8e1673fc6f2e03695f10c7d12335d20daee0c9792d687e9683afd2519dd68f', '61af31139183fb0649315d30d9b858e54b4125c66d427fe4626a90f4c82469b6'),

    ('7a651c441815e6e84f3f9e834d3d4edc5d0e3d994a8444c897e0b19d6ef611e8', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package has left an interim facility', 'Pune, IN',
     '2024-04-03 04:06:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', '8f8e1673fc6f2e03695f10c7d12335d20daee0c9792d687e9683afd2519dd68f', '6a7a026ad44558fe5eed2d5d28a2d2cda39918380871895d4917c1b1005bd2e7', '66ed36b8f2b30d7a4eccddb8c6373c51f7a04322e145bd14b0016908cd08c2e6'),

    ('fbf03581636cd0792762270e01535adb3439cc3706c2fd579d09782f10f10f37', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Package arrived at the final delivery station', 'Mumbai, IN',
     '2024-04-04 07:42:00', 'LogisticsCo', 5.5, '50x20x10 cm',
     '', '6a7a026ad44558fe5eed2d5d28a2d2cda39918380871895d4917c1b1005bd2e7', '74061b8433061695b4132f4aa224d9e6370aa984491a01f2952dbc414eabbf5e', '5fc5e325ede1e09e3421b5bd1b5c70da44e4de006b6e39319674ea5507f08650'),

    ('0617746600e8ae61ff147d12f48607ab99f8c613915feb5834e7766b3913fbeb', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Out for delivery', 'Mumbai, IN',
     '2024-04-05 11:10:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', '74061b8433061695b4132f4aa224d9e6370aa984491a01f2952dbc414eabbf5e', '49eb4171fb0cdf15f44690b7ae583e100d3f67c02a6d7f729a0b788215f8711b', '02ca4dca94813f919faf21730b62d7f14b61e97d596568092d2c7fb3083a012a'),

    ('d96bf33a462451e02200dfb0d6778f0f3a3f1dba64a2878f924cb19e4cc477e6', 'SHIP001', 'TRACK340274928915',
     'ORD40597892194758711', 'Delivered', 'Mumbai, IN',
     '2024-04-05 16:48:00', 'LogisticsCo', 5.5, '50x30x10 cm',
     '', '49eb4171fb0cdf15f44690b7ae583e100d3f67c02a6d7f729a0b788215f8711b', '52113462100cd021525a0b656dbc50fb299eb36b5d21b65ab895fae4106beb71', '134e57c2bfd31f686f812e1be70e46b8ef2a46c49a781454221475e6133abd97');

-- Inserting ShipmentHistory for SHIP003
INSERT INTO ShipmentHistory (HistoryID, ShipmentID, TrackingID, OrderRefNo, StatusUpdate,
                             CurrentLocation, TimeStamp, CarrierName, Weight, Dimensions,
                             Comments, PreviousHash, RecordHash, BlockID)
VALUES 
    ('hist008', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Carrier picked up the package', 'Mumbai, IN',
     '2024-04-28 09:00:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'None', 'hash008', 'block020'),

    ('hist009', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Package has left the origin facility', 'Mumbai, IN',
     '2024-04-28 12:00:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash008', 'hash009', 'block021'),

    ('hist010', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Package arrived at an interim facility', 'Nagpur, IN',
     '2024-04-29 15:30:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash009', 'hash010', 'block022'),

    ('hist011', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Package has left an interim facility', 'Nagpur, IN',
     '2024-04-30 10:15:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash010', 'hash011', 'block023'),

    ('hist012', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Package arrived at the final delivery station', 'Delhi, IN',
     '2024-05-01 14:45:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash011', 'hash012', 'block024'),

    ('hist013', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Out for delivery', 'Delhi, IN',
     '2024-05-02 08:30:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash012', 'hash013', 'block025'),

    ('hist014', 'SHIP003', 'TRACK340374928920', 'ORD40599992194758712', 'Delivered', 'Delhi, IN',
     '2024-05-02 12:00:00', 'LogisticsCo', 3.2, '30x15x5 cm',
     '', 'hash013', 'hash014', 'block026');

-- ============================
-- 10. SmartContracts Table
-- ============================
-- Inserting SmartContracts with Complete Code

INSERT INTO SmartContracts (ContractID, ContractName, Description, Code, TriggerEvent, CreatedBy) VALUES 
    ('SC001', 'Integrity Verification', 'Performs integrity checks on shipment data to ensure consistency and prevent tampering.', 
    'pragma solidity ^0.8.0;
    
    contract IntegrityVerification {
        event IntegrityChecked(string trackingID, bool isValid);
    
        // Function to verify integrity by comparing previous and current hashes
        function verifyIntegrity(string memory trackingID, string memory previousHash, string memory currentHash) public {
            // Simple comparison logic (to be replaced with actual hash comparison logic)
            bool isValid = keccak256(abi.encodePacked(previousHash)) != keccak256(abi.encodePacked(currentHash));
            emit IntegrityChecked(trackingID, isValid);
        }
    }', 'Integrity Check', 'ADM_AditiS'),

    ('SC002', 'Weight Verification', 'Verifies the weight of shipments at checkpoints to ensure accuracy.', 
    'pragma solidity ^0.8.0;
    
    contract WeightVerification {
        event WeightVerified(string trackingID, uint recordedWeight, uint actualWeight, bool isMatch);
    
        // Function to verify shipment weight
        function verifyWeight(string memory trackingID, uint recordedWeight, uint actualWeight) public {
            bool isMatch = (recordedWeight == actualWeight);
            emit WeightVerified(trackingID, recordedWeight, actualWeight, isMatch);
        }
    }', 'Weight Check', 'ADM_NitinD'),

    ('SC003', 'Shipment Hash Update', 'Updates and verifies shipment hashes to maintain blockchain integrity.', 
    'pragma solidity ^0.8.0;
    
    contract ShipmentHashUpdate {
        event HashUpdated(string trackingID, string newHash);
        event HashVerified(string trackingID, bool isValid);
    
        mapping(string => string) public shipmentHashes;
    
        // Function to update the hash of a shipment
        function updateHash(string memory trackingID, string memory newHash) public {
            shipmentHashes[trackingID] = newHash;
            emit HashUpdated(trackingID, newHash);
        }
    
        // Function to verify the current hash matches the stored hash
        function verifyHash(string memory trackingID, string memory currentHash) public view returns (bool) {
            return keccak256(abi.encodePacked(shipmentHashes[trackingID])) == keccak256(abi.encodePacked(currentHash));
        }
    }', 'Hash Update', 'ADM_SureshD');

-- Inserting BlockchainMetadata
INSERT INTO BlockchainMetadata (LastBlockHash) VALUES 
    ('9ddff002db4d75d47606952a05a7968e7fd4db4b49e88a834b61bea3116d98e9'),
    ('d1de32f0ad737fb30a1bc39b92f1b2373be7ede15969ff7eb1e151dee0db575a'),
    ('6a7a026ad44558fe5eed2d5d28a2d2cda39918380871895d4917c1b1005bd2e7'),
    ('84e79756bcde13053713177333fb92f88897ca11155b91a9013449901eb56798'),
    ('8f8e1673fc6f2e03695f10c7d12335d20daee0c9792d687e9683afd2519dd68f'),
    ('d15612da8dbd3fa22e8dfef5f23dfded38368cf866bb1c1266e4d03a75bf5223'),
    ('5fc5e325ede1e09e3421b5bd1b5c70da44e4de006b6e39319674ea5507f08650'),
    ('134e57c2bfd31f686f812e1be70e46b8ef2a46c49a781454221475e6133abd97'),
    ('02ca4dca94813f919faf21730b62d7f14b61e97d596568092d2c7fb3083a012a'),
    ('d1de32f0ad737fb30a1bc39b92f1b2373be7ede15969ff7eb1e151dee0db575a');

-- Inserting Approvals
INSERT INTO Approvals (ApprovalID, TransactionID, ApproverID) VALUES 
    ('APR001', 'TXN001', 'ADM_AditiS'),
    ('APR002', 'TXN002', 'ADM_NitinD'),
    ('APR003', 'TXN003', 'ADM_KiranIT'),
    ('APR004', 'TXN004', 'ADM_AnjaliN'),
    ('APR005', 'TXN005', 'ADM_SureshD'),
    ('APR006', 'TXN006', 'ADM_AditiS'),
    ('APR007', 'TXN007', 'ADM_NitinD'),
    ('APR008', 'TXN008', 'ADM_KiranIT'),
    ('APR009', 'TXN009', 'ADM_AnjaliN'),
    ('APR010', 'TXN010', 'ADM_SureshD'),
    ('APR011', 'TXN011', 'ADM_AditiS'),
    ('APR012', 'TXN012', 'ADM_NitinD'),
    ('APR013', 'TXN013', 'ADM_KiranIT'),
    ('APR014', 'TXN014', 'ADM_AnjaliN'),
    ('APR015', 'TXN015', 'ADM_SureshD');