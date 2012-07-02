drop database BAD_DATA;
CREATE DATABASE BAD_DATA;
use BAD_DATA;

CREATE TABLE Department (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(127) NOT NULL,
    UNIQUE (id),
    PRIMARY KEY (id)
);

CREATE TABLE Customer (
    id INTEGER NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(127),
    last_name VARCHAR(127),
    department_id INTEGER,
    FOREIGN KEY (department_id)
        REFERENCES Department(id),
    UNIQUE (id),
    PRIMARY KEY (id)
);

CREATE TABLE Computer (
    id INTEGER NOT NULL AUTO_INCREMENT,
    customer_id INTEGER NOT NULL,
    po_number VARCHAR(127),
    hw_type TEXT,
    customization TEXT,
    configured_by TEXT,
    notes TEXT,
    date_ready DATE,
    date_computer_ordered DATE,
    date_deployed DATE,
    date_posted_to_rh_ss DATE,
    image VARCHAR(127),
    is_mac BOOLEAN,
    heaf VARCHAR(10),
    asset_tag VARCHAR(127),
    serial_computer VARCHAR(127),
    change_computer VARCHAR(127),
    FOREIGN KEY (customer_id)
        REFERENCES Customer(id),
    UNIQUE(id),
    PRIMARY KEY (id)

);

CREATE TABLE MAC_Address (
    id INTEGER NOT NULL AUTO_INCREMENT,
    address VARCHAR(32) NOT NULL,
    name VARCHAR(127) NOT NULL,
    computer_id INTEGER NOT NULL,
    INDEX (computer_id),
    FOREIGN KEY (computer_id)
        REFERENCES Computer(id),
    UNIQUE (id),
    PRIMARY KEY (id)
);

