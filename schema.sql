CREATE DATABASE IF NOT EXISTS pnp_receiving;

USE pnp_receiving;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(30) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    barcode VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_code VARCHAR(30) NOT NULL UNIQUE,
    location_name VARCHAR(100) NOT NULL,
    location_type ENUM('Shelf', 'Receiving') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    role ENUM(
        'Store Manager',
        'Floor Manager',
        'Staff Member',
        'Receiving Manager'
    ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,

    product_id INT NOT NULL UNIQUE,
    receiving_location_id INT NOT NULL,
    shelf_location_id INT NOT NULL,

    receiving_qty INT NOT NULL DEFAULT 0,
    shelf_qty INT NOT NULL DEFAULT 0,
    required_shelf_qty INT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (receiving_location_id)
        REFERENCES locations(location_id),

    FOREIGN KEY (shelf_location_id)
        REFERENCES locations(location_id),

    CHECK (receiving_qty >= 0),
    CHECK (shelf_qty >= 0),
    CHECK (required_shelf_qty >= 0)
);

CREATE TABLE replenishment_tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,

    product_id INT NOT NULL,
    shelf_location_id INT NOT NULL,

    created_by INT NOT NULL,
    completed_by INT,

    quantity INT NOT NULL,

    priority ENUM('High', 'Medium', 'Low') NOT NULL,

    status ENUM('Pending', 'Completed', 'Cancelled')
        DEFAULT 'Pending' NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (shelf_location_id)
        REFERENCES locations(location_id),

    FOREIGN KEY (created_by)
        REFERENCES users(user_id),

    FOREIGN KEY (completed_by)
        REFERENCES users(user_id),

    CHECK (quantity > 0),

    CHECK (
        (status = 'Completed'
         AND completed_at IS NOT NULL
         AND completed_by IS NOT NULL)
        OR
        (status <> 'Completed'
         AND completed_at IS NULL
         AND completed_by IS NULL)
    ),

    INDEX idx_task_status_priority (status, priority)
);

CREATE TABLE stock_movements (
    movement_id INT AUTO_INCREMENT PRIMARY KEY,

    product_id INT NOT NULL,
    user_id INT NOT NULL,
    task_id INT UNIQUE,

    movement_type ENUM(
        'Stock Received',
        'Damaged Stock',
        'Stock Reconciliation',
        'Shelf Count Updated',
        'Replenishment'
    ) NOT NULL,

    receiving_before INT NOT NULL,
    receiving_after INT NOT NULL,

    shelf_before INT NOT NULL,
    shelf_after INT NOT NULL,

    reason VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (task_id)
        REFERENCES replenishment_tasks(task_id),

    CHECK (receiving_before >= 0),
    CHECK (receiving_after >= 0),
    CHECK (shelf_before >= 0),
    CHECK (shelf_after >= 0),

    INDEX idx_movement_product_date (product_id, created_at)
);

