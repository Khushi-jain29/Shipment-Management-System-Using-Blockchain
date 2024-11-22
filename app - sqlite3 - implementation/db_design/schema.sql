-- ===================================================
-- Shipment Management and Tracking System Database Schema
-- ===================================================

-- ============================
-- 1. Companies Table
-- ============================
CREATE TABLE Companies (
    CompanyID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName TEXT NOT NULL UNIQUE,
    Description TEXT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- 2. Users Table
-- ============================
CREATE TABLE Users (
    UserID TEXT PRIMARY KEY,
    UserName TEXT NOT NULL,
    UserType TEXT NOT NULL CHECK (UserType IN ('Consumer', 'Seller', 'Logistics', 'Administrator')),
    Password TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    ContactNum TEXT,
    CompanyID INTEGER, -- Optional, foreign key if linking to a Companies table
    RegistrationDate DATE NOT NULL
);

-- ============================
-- 3. Roles Table
-- ============================
CREATE TABLE Roles (
    RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleName TEXT NOT NULL UNIQUE
);

-- ============================
-- 4. Permissions Table
-- ============================
CREATE TABLE Permissions (
    PermissionID INTEGER PRIMARY KEY AUTOINCREMENT,
    PermissionName TEXT NOT NULL UNIQUE
);

-- ============================
-- 5. RolePermissions Table
-- ============================
CREATE TABLE RolePermissions (
    RoleID INTEGER REFERENCES Roles(RoleID) ON DELETE CASCADE,
    PermissionID INTEGER REFERENCES Permissions(PermissionID) ON DELETE CASCADE,
    PRIMARY KEY (RoleID, PermissionID)
);

-- ============================
-- 6. UserRoles Table
-- ============================
CREATE TABLE UserRoles (
    UserID TEXT REFERENCES Users(UserID) ON DELETE CASCADE,
    RoleID INTEGER REFERENCES Roles(RoleID) ON DELETE CASCADE,
    PRIMARY KEY (UserID, RoleID)
);

-- ============================
-- 7. Products Table
-- ============================
CREATE TABLE Products (
    ProductID TEXT PRIMARY KEY,
    SellerID TEXT,
    ProductName TEXT NOT NULL,
    ProductDescription TEXT,
    Price REAL,
    Brand TEXT,
    Category TEXT,
    ModelName TEXT,
    ShipsFrom TEXT,
    SoldBy TEXT,
    WarrantyPolicy TEXT,
    ProductImageUrl TEXT,
    AdditionalFeatures TEXT
);

-- ============================
-- 8. Shipments Table
-- ============================
CREATE TABLE Shipments (
    ShipmentID TEXT PRIMARY KEY,
    TrackingID TEXT UNIQUE NOT NULL,
    OrderRefNo TEXT UNIQUE,
    ProductID TEXT,
    CustomerID TEXT,
    InitialStatus TEXT NOT NULL CHECK (InitialStatus IN ('Order Created', 'In Transit', 'Delivered', 'Cancelled')),
    EstimatedDeliveryDate DATE,
    Origin TEXT,
    Destination TEXT,
    Weight REAL,
    Dimensions TEXT
);

-- ============================
-- 9. ShipmentHistory Table
-- ============================
CREATE TABLE ShipmentHistory (
    HistoryID TEXT PRIMARY KEY,
    ShipmentID TEXT,
    TrackingID TEXT,
    OrderRefNo TEXT,
    StatusUpdate TEXT,
    CurrentLocation TEXT,
    TimeStamp DATETIME NOT NULL,
    CarrierName TEXT,
    Weight REAL,
    Dimensions TEXT,
    Comments TEXT,
    PreviousHash TEXT,
    RecordHash TEXT,
    BlockID TEXT,
    CreatedBy TEXT,
    VerifiedBy TEXT,
    ChangeLog TEXT
);

-- ============================
-- 10. SmartContracts Table
-- ============================
CREATE TABLE SmartContracts (
    ContractID TEXT PRIMARY KEY,
    ContractName TEXT NOT NULL,
    Description TEXT,
    Code TEXT NOT NULL,
    TriggerEvent TEXT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    CreatedBy TEXT REFERENCES Users(UserID)
);

-- ============================
-- 11. BlockchainMetadata Table
-- ============================
CREATE TABLE BlockchainMetadata (
    MetadataID INTEGER PRIMARY KEY AUTOINCREMENT,
    LastBlockHash TEXT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- 12. Approvals Table
-- ============================
CREATE TABLE Approvals (
    ApprovalID TEXT PRIMARY KEY,
    TransactionID TEXT NOT NULL,
    ApproverID TEXT REFERENCES Users(UserID),
    ApprovalTime DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ============================
-- 13. SupportTickets Table
-- ============================
CREATE TABLE SupportTickets (
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT NOT NULL,
    Subject TEXT NOT NULL,
    Message TEXT NOT NULL,
    TimeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);


-- ============================
-- 14. Notifications Table
-- ============================

CREATE TABLE Notifications (
    NotificationID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT NOT NULL,
    Message TEXT NOT NULL,
    TimeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
