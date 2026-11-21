"""
Pick n Pay Wolmaransstad - Receiving Stock System
Flask web application and REST API.
Group 22
"""

from flask import Blueprint, jsonify, request, current_app
from db import get_db_connection
from contextlib import contextmanager
from EOQ import calculate_eoq, total_annual_cost, items_in_inventory

import mysql.connector



api = Blueprint("api", __name__)


# Configure application logging



# Database connection management

@contextmanager
def database_cursor():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True,
            buffered=True
        )

        yield connection, cursor

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:

            if connection.in_transaction:
                connection.rollback()

            connection.close()


# Centralised API error handling

class APIError(Exception):

    def __init__(self, message, status_code=400):

        self.message = message
        self.status_code = status_code

        super().__init__(message)


@api.app_errorhandler(APIError)
def handle_api_error(error):

    current_app.logger.warning(error.message)

    return jsonify({
        "error": error.message
    }), error.status_code


@api.app_errorhandler(mysql.connector.Error)
def handle_database_error(error):

    current_app.logger.exception("Database operation failed")

    if error.errno == 1062:

        return jsonify({
            "error": "A record with these unique details already exists."
        }), 400

    return jsonify({
        "error": "A database error occurred."
    }), 500


@api.app_errorhandler(404)
def handle_not_found(error):

    return jsonify({
        "error": "The requested resource was not found."
    }), 404


@api.app_errorhandler(405)
def handle_method_not_allowed(error):

    return jsonify({
        "error": "HTTP method not allowed."
    }), 405


@api.app_errorhandler(500)
def handle_internal_error(error):

    current_app.logger.error("Internal server error: %s", error)

    return jsonify({
        "error": "An internal server error occurred."
    }), 500


# Validate incoming JSON data

def get_request_data():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        raise APIError("Invalid JSON request.")

    return data


# Validate integer values

def validate_integer(value, field_name, minimum=0):

    if type(value) is not int:

        raise APIError(field_name + " must be an integer.")

    if value < minimum or value > 2147483647:

        raise APIError(field_name + " is outside the valid range.")

    return value


# Validate text values

def validate_text(value, field_name, max_length):

    if not isinstance(value, str) or not value.strip():

        raise APIError(field_name + " is required.")

    value = value.strip()

    if len(value) > max_length:

        raise APIError(field_name + " is too long.")

    return value


# Validate product name

def validate_product_name(value):

    name = validate_text(value, "Product name", 150)

    if any(character in name for character in '<>"'):

        raise APIError("Invalid product name.")

    return name


# Retrieve a selected system user

def find_user(cursor, username):

    username = validate_text(username, "Username", 50)

    cursor.execute("""
        SELECT user_id, full_name, username, role
        FROM users
        WHERE username = %s
    """, (username,))

    user = cursor.fetchone()

    if user is None:

        raise APIError("User not found.", 404)

    return user


# Convert database timestamps into JSON-compatible values

def format_dates(record):

    for field in ["created_at", "completed_at", "updated_at"]:

        if field in record and record[field] is not None:

            record[field] = record[field].isoformat()

    return record



# --------------------------------------------------
# PRODUCT API ENDPOINTS
# --------------------------------------------------


# Base query for products and inventory information

PRODUCT_QUERY = """
    SELECT
        p.product_id,
        p.product_code,
        p.product_name,
        p.barcode,
        i.shelf_qty,
        i.required_shelf_qty,
        i.receiving_qty,
        i.shelf_location_id,
        i.receiving_location_id,

        GREATEST(
            0, i.required_shelf_qty - i.shelf_qty
        ) AS quantity_needed,

        s.location_name AS shelf_location,
        r.location_name AS receiving_location

    FROM products p

    JOIN inventory i
        ON p.product_id = i.product_id

    JOIN locations s
        ON i.shelf_location_id = s.location_id

    JOIN locations r
        ON i.receiving_location_id = r.location_id
"""


# Retrieve products with optional pagination and filtering

@api.route("/api/products", methods=["GET"])
def get_products():

    search = request.args.get("search", "").strip()

    status = request.args.get("status", "").strip().lower()

    page = request.args.get("page")

    size = request.args.get("size")

    # Validate search and status parameters

    if len(search) > 150:

        raise APIError("Search term is too long.")

    if status not in [
        "",
        "sufficient",
        "insufficient",
        "out_of_stock"
    ]:

        raise APIError("Invalid stock status.")

    # Validate pagination

    try:

        if page is not None or size is not None:

            page = int(page) if page is not None else 1

            size = int(size) if size is not None else 10

            if not 1 <= page <= 100000:

                raise APIError("Page must be between 1 and 100000.")

            if not 1 <= size <= 100:

                raise APIError("Page size must be between 1 and 100.")

    except ValueError:

        raise APIError("Page and size must be integers.")

    query = PRODUCT_QUERY + " WHERE 1 = 1"

    parameters = []

    # Filter by name, product code or barcode

    if search:

        query += """
            AND (
                p.product_name LIKE %s
                OR p.product_code LIKE %s
                OR p.barcode LIKE %s
            )
        """

        search_value = "%" + search + "%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    # Filter by stock availability

    if status == "sufficient":

        query += """
            AND i.receiving_qty > 0
            AND i.receiving_qty >= GREATEST(
                0, i.required_shelf_qty - i.shelf_qty
            )
        """

    elif status == "insufficient":

        query += """
            AND i.receiving_qty > 0
            AND i.receiving_qty < GREATEST(
                0, i.required_shelf_qty - i.shelf_qty
            )
        """

    elif status == "out_of_stock":

        query += """
            AND i.receiving_qty = 0
        """

    query += " ORDER BY p.product_code"

    # Apply pagination only when requested

    if page is not None:

        offset = (page - 1) * size

        query += " LIMIT %s OFFSET %s"

        parameters.extend([size, offset])

    with database_cursor() as (connection, cursor):

        cursor.execute(query, tuple(parameters))

        products = cursor.fetchall()

        return jsonify(products), 200


# Retrieve an individual product

@api.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    with database_cursor() as (connection, cursor):

        cursor.execute(
            PRODUCT_QUERY + " WHERE p.product_id = %s",
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:

            raise APIError("Product not found.", 404)

        return jsonify(product), 200


# Create a new product

@api.route("/api/products", methods=["POST"])
def create_product():

    data = get_request_data()

    product_code = validate_text(
        data.get("product_code"),
        "Product code",
        30
    )

    product_name = validate_product_name(
        data.get("product_name")
    )

    receiving_location_id = validate_integer(
        data.get("receiving_location_id"),
        "Receiving location ID",
        1
    )

    shelf_location_id = validate_integer(
        data.get("shelf_location_id"),
        "Shelf location ID",
        1
    )

    required_shelf_qty = validate_integer(
        data.get("required_shelf_qty", 0),
        "Required shelf quantity"
    )

    barcode = data.get("barcode")

    if barcode is not None:

        barcode = validate_text(barcode, "Barcode", 50)

    with database_cursor() as (connection, cursor):

        connection.start_transaction()

        # Validate receiving location

        cursor.execute("""
            SELECT location_id
            FROM locations
            WHERE location_id = %s
            AND location_type = 'Receiving'
        """, (receiving_location_id,))

        if cursor.fetchone() is None:

            raise APIError("Receiving location not found.")

        # Validate shelf location

        cursor.execute("""
            SELECT location_id
            FROM locations
            WHERE location_id = %s
            AND location_type = 'Shelf'
        """, (shelf_location_id,))

        if cursor.fetchone() is None:

            raise APIError("Shelf location not found.")

        # Create product

        cursor.execute("""
            INSERT INTO products (
                product_code,
                product_name,
                barcode
            )
            VALUES (%s, %s, %s)
        """, (
            product_code,
            product_name,
            barcode
        ))

        product_id = cursor.lastrowid

        # Create inventory record

        cursor.execute("""
            INSERT INTO inventory (
                product_id,
                receiving_location_id,
                shelf_location_id,
                receiving_qty,
                shelf_qty,
                required_shelf_qty
            )
            VALUES (%s, %s, %s, 0, 0, %s)
        """, (
            product_id,
            receiving_location_id,
            shelf_location_id,
            required_shelf_qty
        ))

        connection.commit()

        current_app.logger.info(
            "Product created: %s", product_id
        )

        return jsonify({
            "message": "Product created successfully.",
            "product_id": product_id
        }), 201


# Update an existing product

@api.route("/api/products/<int:product_id>", methods=["PATCH"])
def update_product(product_id):

    data = get_request_data()

    allowed_fields = {
        "product_name",
        "product_code",
        "barcode"
    }

    if not data or not set(data).issubset(allowed_fields):

        raise APIError("Invalid product update fields.")

    with database_cursor() as (connection, cursor):

        connection.start_transaction()

        cursor.execute("""
            SELECT product_name, product_code, barcode
            FROM products
            WHERE product_id = %s
            FOR UPDATE
        """, (product_id,))

        product = cursor.fetchone()

        if product is None:

            raise APIError("Product not found.", 404)

        product_name = validate_product_name(
            data.get("product_name", product["product_name"])
        )

        product_code = validate_text(
            data.get("product_code", product["product_code"]),
            "Product code",
            30
        )

        barcode = data.get("barcode", product["barcode"])

        if barcode is not None:

            barcode = validate_text(barcode, "Barcode", 50)

        cursor.execute("""
            UPDATE products

            SET product_name = %s,
                product_code = %s,
                barcode = %s

            WHERE product_id = %s
        """, (
            product_name,
            product_code,
            barcode,
            product_id
        ))

        connection.commit()

        current_app.logger.info(
            "Product updated: %s", product_id
        )

        return jsonify({
            "message": "Product updated successfully.",
            "product_id": product_id
        }), 200


# --------------------------------------------------
# REPLENISHMENT TASK API ENDPOINTS
# --------------------------------------------------


# Base query for replenishment tasks

TASK_QUERY = """
    SELECT
        t.task_id,
        t.product_id,
        p.product_name,
        t.quantity,
        t.priority,
        t.status,
        l.location_name,
        creator.full_name AS created_by,
        employee.full_name AS completed_by,
        t.created_at,
        t.completed_at

    FROM replenishment_tasks t

    JOIN products p
        ON t.product_id = p.product_id

    JOIN locations l
        ON t.shelf_location_id = l.location_id

    JOIN users creator
        ON t.created_by = creator.user_id

    LEFT JOIN users employee
        ON t.completed_by = employee.user_id
"""


# Retrieve all replenishment tasks

@api.route("/api/tasks", methods=["GET"])
def get_tasks():

    status = request.args.get("status", "").strip().lower()

    priority = request.args.get("priority", "").strip().lower()

    if status not in ["", "pending", "completed", "cancelled"]:

        raise APIError("Invalid task status.")

    if priority not in ["", "high", "medium", "low"]:

        raise APIError("Invalid task priority.")

    query = TASK_QUERY + " WHERE 1 = 1"

    parameters = []

    if status:

        query += " AND LOWER(t.status) = %s"

        parameters.append(status)

    if priority:

        query += " AND LOWER(t.priority) = %s"

        parameters.append(priority)

    query += " ORDER BY t.created_at DESC, t.task_id DESC"

    with database_cursor() as (connection, cursor):

        cursor.execute(query, tuple(parameters))

        tasks = cursor.fetchall()

        return jsonify([
            format_dates(task) for task in tasks
        ]), 200


# Retrieve an individual replenishment task

@api.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    with database_cursor() as (connection, cursor):

        cursor.execute(
            TASK_QUERY + " WHERE t.task_id = %s",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:

            raise APIError("Replenishment task not found.", 404)

        return jsonify(format_dates(task)), 200


# Create a new replenishment task

@api.route("/api/tasks", methods=["POST"])
def create_task():

    data = get_request_data()

    product_id = validate_integer(
        data.get("product_id"),
        "Product ID",
        1
    )

    quantity = validate_integer(
        data.get("quantity"),
        "Quantity",
        1
    )

    priority = data.get("priority")

    username = data.get("username")

    if priority not in ["High", "Medium", "Low"]:

        raise APIError("Invalid priority.")

    with database_cursor() as (connection, cursor):

        connection.start_transaction()

        # Retrieve and lock inventory

        cursor.execute("""
            SELECT
                receiving_qty,
                shelf_qty,
                required_shelf_qty,
                shelf_location_id

            FROM inventory

            WHERE product_id = %s
            FOR UPDATE
        """, (product_id,))

        inventory = cursor.fetchone()

        if inventory is None:

            raise APIError("Product not found.", 404)

        quantity_needed = max(
            0,
            inventory["required_shelf_qty"] -
            inventory["shelf_qty"]
        )

        if quantity > inventory["receiving_qty"]:

            raise APIError("Insufficient receiving stock.")

        if quantity > quantity_needed:

            raise APIError("Quantity exceeds shelf requirement.")

        # Prevent duplicate pending tasks

        cursor.execute("""
            SELECT task_id
            FROM replenishment_tasks
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))

        if cursor.fetchone() is not None:

            raise APIError("A pending task already exists.")

        user = find_user(cursor, username)

        # Insert replenishment task

        cursor.execute("""
            INSERT INTO replenishment_tasks (
                product_id,
                shelf_location_id,
                created_by,
                quantity,
                priority,
                status
            )
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """, (
            product_id,
            inventory["shelf_location_id"],
            user["user_id"],
            quantity,
            priority
        ))

        task_id = cursor.lastrowid

        connection.commit()

        current_app.logger.info(
            "Replenishment task created: %s", task_id
        )

        return jsonify({
            "message": "Replenishment task created.",
            "task_id": task_id
        }), 201


# Complete a replenishment task

@api.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def complete_task(task_id):

    data = get_request_data()

    username = data.get("username")

    with database_cursor() as (connection, cursor):

        connection.start_transaction()

        # Identify product

        cursor.execute("""
            SELECT product_id
            FROM replenishment_tasks
            WHERE task_id = %s
        """, (task_id,))

        task_product = cursor.fetchone()

        if task_product is None:

            raise APIError("Task not found.", 404)

        # Lock inventory

        cursor.execute("""
            SELECT
                receiving_qty,
                shelf_qty,
                required_shelf_qty

            FROM inventory

            WHERE product_id = %s
            FOR UPDATE
        """, (task_product["product_id"],))

        inventory = cursor.fetchone()

        if inventory is None:

            raise APIError("Inventory record not found.", 404)

        # Lock task

        cursor.execute("""
            SELECT
                task_id,
                product_id,
                quantity,
                status

            FROM replenishment_tasks

            WHERE task_id = %s
            FOR UPDATE
        """, (task_id,))

        task = cursor.fetchone()

        if task is None:

            raise APIError("Task not found.", 404)

        if task["status"] != "Pending":

            raise APIError("This task is no longer pending.")

        employee = find_user(cursor, username)

        quantity = task["quantity"]

        receiving_before = inventory["receiving_qty"]

        shelf_before = inventory["shelf_qty"]

        quantity_needed = max(
            0,
            inventory["required_shelf_qty"] - shelf_before
        )

        # Validate stock availability

        if quantity > receiving_before:

            raise APIError("Insufficient receiving stock.")

        if quantity > quantity_needed:

            raise APIError("Quantity exceeds shelf requirement.")

        receiving_after = receiving_before - quantity

        shelf_after = shelf_before + quantity

        # Update stock quantities

        cursor.execute("""
            UPDATE inventory

            SET receiving_qty = %s,
                shelf_qty = %s

            WHERE product_id = %s
        """, (
            receiving_after,
            shelf_after,
            task["product_id"]
        ))

        # Complete the task

        cursor.execute("""
            UPDATE replenishment_tasks

            SET status = 'Completed',
                completed_by = %s,
                completed_at = NOW()

            WHERE task_id = %s
        """, (
            employee["user_id"],
            task_id
        ))

        # Record movement in audit history

        cursor.execute("""
            INSERT INTO stock_movements (
                product_id,
                user_id,
                task_id,
                movement_type,
                receiving_before,
                receiving_after,
                shelf_before,
                shelf_after,
                reason
            )
            VALUES (
                %s, %s, %s, 'Replenishment',
                %s, %s, %s, %s, %s
            )
        """, (
            task["product_id"],
            employee["user_id"],
            task_id,
            receiving_before,
            receiving_after,
            shelf_before,
            shelf_after,
            "Stock moved from receiving to the shop floor."
        ))

        connection.commit()

        current_app.logger.info(
            "Replenishment task completed: %s", task_id
        )

        return jsonify({
            "message": "Replenishment task completed.",
            "receiving_qty": receiving_after,
            "shelf_qty": shelf_after
        }), 200


# --------------------------------------------------
# INVENTORY CONTROL
# --------------------------------------------------


# Update inventory quantities

@api.route("/api/inventory/<int:product_id>", methods=["PATCH"])
def update_inventory(product_id):

    data = get_request_data()

    action = data.get("action")

    quantity = validate_integer(
        data.get("quantity"),
        "Quantity"
    )

    username = data.get("username")

    reason = validate_text(
        data.get("reason"),
        "Transaction reason",
        255
    )

    if action not in [
        "receive",
        "damage",
        "reconcile",
        "shelf"
    ]:

        raise APIError("Invalid transaction type.")

    if action in ["receive", "damage"] and quantity == 0:

        raise APIError("Quantity must be greater than zero.")

    with database_cursor() as (connection, cursor):

        connection.start_transaction()

        cursor.execute("""
            SELECT receiving_qty, shelf_qty
            FROM inventory
            WHERE product_id = %s
            FOR UPDATE
        """, (product_id,))

        inventory = cursor.fetchone()

        if inventory is None:

            raise APIError("Product not found.", 404)

        user = find_user(cursor, username)

        receiving_before = inventory["receiving_qty"]

        shelf_before = inventory["shelf_qty"]

        receiving_after = receiving_before

        shelf_after = shelf_before

        # Receive stock

        if action == "receive":

            receiving_after += quantity

            movement_type = "Stock Received"

        # Record damaged stock

        elif action == "damage":

            if quantity > receiving_before:

                raise APIError(
                    "Damaged quantity exceeds available stock."
                )

            receiving_after -= quantity

            movement_type = "Damaged Stock"

        # Reconcile stock

        elif action == "reconcile":

            receiving_after = quantity

            movement_type = "Stock Reconciliation"

        # Update shelf quantity

        elif action == "shelf":

            shelf_after = quantity

            movement_type = "Shelf Count Updated"

        if receiving_after > 2147483647:

            raise APIError("Receiving quantity is too large.")

        # Update inventory

        cursor.execute("""
            UPDATE inventory

            SET receiving_qty = %s,
                shelf_qty = %s

            WHERE product_id = %s
        """, (
            receiving_after,
            shelf_after,
            product_id
        ))

        # Record the stock movement

        cursor.execute("""
            INSERT INTO stock_movements (
                product_id,
                user_id,
                movement_type,
                receiving_before,
                receiving_after,
                shelf_before,
                shelf_after,
                reason
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product_id,
            user["user_id"],
            movement_type,
            receiving_before,
            receiving_after,
            shelf_before,
            shelf_after,
            reason
        ))

        connection.commit()

        current_app.logger.info(
            "Inventory updated: product %s, action %s",
            product_id,
            action
        )

        return jsonify({
            "message": "Stock transaction recorded successfully.",
            "receiving_qty": receiving_after,
            "shelf_qty": shelf_after
        }), 200


# Retrieve stock movement history

@api.route("/api/stock-movements", methods=["GET"])
def get_stock_movements():

    with database_cursor() as (connection, cursor):

        cursor.execute("""
            SELECT
                m.movement_id,
                p.product_name,
                u.full_name,
                m.movement_type,
                m.receiving_before,
                m.receiving_after,
                m.shelf_before,
                m.shelf_after,
                m.reason,
                m.created_at

            FROM stock_movements m

            JOIN products p
                ON m.product_id = p.product_id

            JOIN users u
                ON m.user_id = u.user_id

            ORDER BY m.created_at DESC, m.movement_id DESC
        """)

        movements = cursor.fetchall()

        return jsonify([
            format_dates(movement)
            for movement in movements
        ]), 200


# --------------------------------------------------
# USERS
# --------------------------------------------------


# Retrieve system users

@api.route("/api/users", methods=["GET"])
def get_users():

    with database_cursor() as (connection, cursor):

        cursor.execute("""
            SELECT
                user_id,
                full_name,
                username,
                role

            FROM users

            ORDER BY user_id
        """)

        users = cursor.fetchall()

        return jsonify(users), 200


# --------------------------------------------------
# LOCATIONS
# --------------------------------------------------


# Retrieve shelf and receiving locations

@api.route("/api/locations", methods=["GET"])
def get_locations():

    location_type = request.args.get("type", "").strip().lower()

    if location_type not in ["", "shelf", "receiving"]:

        raise APIError("Invalid location type.")

    query = """
        SELECT
            location_id,
            location_code,
            location_name,
            location_type

        FROM locations
        WHERE 1 = 1
    """

    parameters = []

    if location_type:

        query += " AND LOWER(location_type) = %s"

        parameters.append(location_type)

    query += " ORDER BY location_code"

    with database_cursor() as (connection, cursor):

        cursor.execute(query, tuple(parameters))

        return jsonify(cursor.fetchall()), 200


# --------------------------------------------------
# DASHBOARD AND PERFORMANCE METRICS
# --------------------------------------------------


# Retrieve dashboard KPIs

@api.route("/api/dashboard", methods=["GET"])
def get_dashboard():

    with database_cursor() as (connection, cursor):

        # Inventory KPIs

        cursor.execute("""
            SELECT
                COUNT(*) AS total_products,

                COALESCE(
                    SUM(receiving_qty), 0
                ) AS total_receiving_stock,

                COALESCE(SUM(
                    CASE
                        WHEN receiving_qty < GREATEST(
                            0, required_shelf_qty - shelf_qty
                        )
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS insufficient_items,

                COALESCE(SUM(
                    CASE
                        WHEN receiving_qty >= GREATEST(
                            0, required_shelf_qty - shelf_qty
                        )
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS sufficient_items,

                COALESCE(SUM(
                    CASE
                        WHEN receiving_qty = 0
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS out_of_stock_items

            FROM inventory
        """)

        inventory = cursor.fetchone()

        # Replenishment task KPIs

        cursor.execute("""
            SELECT
                COUNT(*) AS total_tasks,

                COALESCE(SUM(
                    CASE
                        WHEN status = 'Pending'
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS pending_tasks,

                COALESCE(SUM(
                    CASE
                        WHEN status = 'Completed'
                        AND DATE(completed_at) = CURDATE()
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS completed_today,

                AVG(
                    CASE
                        WHEN status = 'Completed'
                        THEN TIMESTAMPDIFF(
                            SECOND,
                            created_at,
                            completed_at
                        ) / 60.0
                    END
                ) AS average_response_time

            FROM replenishment_tasks
        """)

        performance = cursor.fetchone()

        # Inventory accuracy KPIs

        cursor.execute("""
            SELECT
                COUNT(*) AS total_reconciliations,

                COALESCE(SUM(
                    CASE
                        WHEN receiving_before = receiving_after
                        THEN 1
                        ELSE 0
                    END
                ), 0) AS accurate_reconciliations

            FROM stock_movements

            WHERE movement_type = 'Stock Reconciliation'
        """)

        accuracy = cursor.fetchone()

        total_reconciliations = accuracy["total_reconciliations"]

        accurate_reconciliations = int(
            accuracy["accurate_reconciliations"]
        )

        discrepancies = (
            total_reconciliations - accurate_reconciliations
        )

        inventory_accuracy = None

        if total_reconciliations > 0:

            inventory_accuracy = round(
                accurate_reconciliations /
                total_reconciliations * 100,
                2
            )

        average_response = performance["average_response_time"]

        if average_response is not None:

            average_response = round(
                float(average_response), 2
            )

        return jsonify({

            "total_products":
                inventory["total_products"],

            "total_receiving_stock":
                int(inventory["total_receiving_stock"]),

            "insufficient_items":
                int(inventory["insufficient_items"]),

            "sufficient_items":
                int(inventory["sufficient_items"]),

            "out_of_stock_items":
                int(inventory["out_of_stock_items"]),

            "total_tasks":
                performance["total_tasks"],

            "pending_tasks":
                int(performance["pending_tasks"]),

            "completed_today":
                int(performance["completed_today"]),

            "average_response_time":
                average_response,

            "total_reconciliations":
                total_reconciliations,

            "discrepancies":
                discrepancies,

            "inventory_accuracy":
                inventory_accuracy

        }), 200

# Economic Order Quantity recommendation

@api.route("/api/products/<int:product_id>/eoq", methods=["GET"])
def get_product_eoq(product_id):

    with database_cursor() as (connection, cursor):

        cursor.execute("""
            SELECT product_id, product_name
            FROM products
            WHERE product_id = %s
        """, (product_id,))

        product = cursor.fetchone()

        if product is None:

            raise APIError("Product not found.", 404)

        product_name = product["product_name"]

        # Retrieve estimated EOQ input parameters

        model_data = items_in_inventory.get(product_name)

        if model_data is None:

            return jsonify({

                "available": False,
                "message": "EOQ input data is not available for this product."

            }), 200

        annual_demand = model_data["demand"]

        ordering_cost = model_data["ordering_cost"]

        holding_cost = model_data["holding_cost"]

        # Calculate EOQ using the existing supply chain model

        eoq = calculate_eoq(
            annual_demand,
            ordering_cost,
            holding_cost
        )

        orders_per_year = annual_demand / eoq

        days_between_orders = 365 / orders_per_year

        annual_cost = total_annual_cost(
            annual_demand,
            ordering_cost,
            holding_cost,
            eoq
        )

        return jsonify({

            "available": True,

            "product_id": product_id,

            "product_name": product_name,

            "annual_demand": annual_demand,

            "ordering_cost": ordering_cost,

            "holding_cost": holding_cost,

            "eoq": round(eoq, 2),

            "recommended_quantity": max(1, round(eoq)),

            "orders_per_year": round(orders_per_year, 2),

            "days_between_orders": round(days_between_orders, 2),

            "total_annual_cost": round(annual_cost, 2),

            "data_source": "Estimated prototype model inputs"

        }), 200
