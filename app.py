"""
Pick n Pay Wolmaransstad - Receiving Stock System
Flask web application and API.
"""

from flask import Flask, jsonify, render_template, request
from db import get_db_connection
import mysql.connector

app = Flask(__name__)


# Home page

@app.route("/")
def home():

    return render_template("index.html")


# Retrieve inventory from MySQL

@app.route("/api/products", methods=["GET"])
def get_products():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_code,
                p.product_name,
                p.barcode,
                i.shelf_qty,
                i.required_shelf_qty,
                i.receiving_qty,
                i.shelf_location_id,
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

            ORDER BY p.product_code
        """)

        products = cursor.fetchall()

        return jsonify(products), 200

    except mysql.connector.Error:

        app.logger.exception("Could not retrieve products")

        return jsonify({
            "error": "Unable to retrieve inventory."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

# Retrieve replenishment tasks from MySQL

@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
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

            ORDER BY t.created_at DESC
        """)

        tasks = cursor.fetchall()

        for task in tasks:

            task["created_at"] = task["created_at"].isoformat()

            if task["completed_at"] is not None:

                task["completed_at"] = task["completed_at"].isoformat()

        return jsonify(tasks), 200

    except mysql.connector.Error:

        app.logger.exception("Unable to retrieve tasks")

        return jsonify({
            "error": "Unable to retrieve replenishment tasks."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

# Create a new replenishment task

@app.route("/api/tasks", methods=["POST"])
def create_task():

    connection = None
    cursor = None

    data = request.get_json(silent=True) or {}

    product_id = data.get("product_id")
    quantity = data.get("quantity")
    priority = data.get("priority")
    username = data.get("username")

    # Validate the submitted information

    if type(product_id) is not int or product_id <= 0:

        return jsonify({
            "error": "Invalid product."
        }), 400

    if type(quantity) is not int or quantity <= 0:

        return jsonify({
            "error": "Enter a valid quantity."
        }), 400

    if priority not in ["High", "Medium", "Low"]:

        return jsonify({
            "error": "Invalid priority."
        }), 400

    if not isinstance(username, str) or not username.strip():

        return jsonify({
            "error": "Please select a user."
        }), 400

    try:

        connection = get_db_connection()

        connection.start_transaction()

        cursor = connection.cursor(dictionary=True)

        # Retrieve current inventory quantities

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

            return jsonify({
                "error": "Product not found."
            }), 404

        quantity_needed = max(
            0,
            inventory["required_shelf_qty"] -
            inventory["shelf_qty"]
        )

        if quantity > inventory["receiving_qty"]:

            return jsonify({
                "error": "Insufficient receiving stock."
            }), 400

        if quantity > quantity_needed:

            return jsonify({
                "error": "Quantity exceeds shelf requirement."
            }), 400

        # Check for an existing pending task

        cursor.execute("""
            SELECT task_id
            FROM replenishment_tasks
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))

        if cursor.fetchone() is not None:

            return jsonify({
                "error": "A pending task already exists."
            }), 400

        # Retrieve the selected user

        cursor.execute("""
            SELECT user_id
            FROM users
            WHERE username = %s
        """, (username,))

        user = cursor.fetchone()

        if user is None:

            return jsonify({
                "error": "User not found."
            }), 404

        # Insert the replenishment task

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

        return jsonify({
            "message": "Replenishment task created.",
            "task_id": task_id
        }), 201

    except mysql.connector.Error:

        app.logger.exception("Unable to create task")

        return jsonify({
            "error": "Unable to create replenishment task."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:

            if connection.in_transaction:
                connection.rollback()

            connection.close()

# Complete an existing replenishment task

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def complete_task(task_id):

    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({
            "error": "Invalid request."
        }), 400

    username = data.get("username")

    if not isinstance(username, str) or not username.strip():

        return jsonify({
            "error": "Please select a user."
        }), 400

    try:

        connection = get_db_connection()

        connection.start_transaction()

        cursor = connection.cursor(dictionary=True)

        # Identify the product associated with the task

        cursor.execute("""
            SELECT product_id
            FROM replenishment_tasks
            WHERE task_id = %s
        """, (task_id,))

        task_product = cursor.fetchone()

        if task_product is None:

            return jsonify({
                "error": "Task not found."
            }), 404

        # Lock the inventory record

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

            return jsonify({
                "error": "Inventory record not found."
            }), 404

        # Lock the replenishment task

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

            return jsonify({
                "error": "Task not found."
            }), 404

        if task["status"] != "Pending":

            return jsonify({
                "error": "This task is no longer pending."
            }), 400

        # Retrieve the selected employee

        cursor.execute("""
            SELECT user_id
            FROM users
            WHERE username = %s
        """, (username,))

        employee = cursor.fetchone()

        if employee is None:

            return jsonify({
                "error": "User not found."
            }), 404

        quantity = task["quantity"]

        receiving_before = inventory["receiving_qty"]

        shelf_before = inventory["shelf_qty"]

        quantity_needed = max(
            0,
            inventory["required_shelf_qty"] - shelf_before
        )

        # Validate stock availability

        if quantity > receiving_before:

            return jsonify({
                "error": "Insufficient receiving stock."
            }), 400

        if quantity > quantity_needed:

            return jsonify({
                "error": "Quantity exceeds the shelf requirement."
            }), 400

        # Calculate updated stock quantities

        receiving_after = receiving_before - quantity

        shelf_after = shelf_before + quantity

        # Update inventory

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

        # Mark replenishment task as completed

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

        # Record stock movement for the audit history

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

        # Save all changes together

        connection.commit()

        return jsonify({
            "message": "Replenishment task completed.",
            "receiving_qty": receiving_after,
            "shelf_qty": shelf_after
        }), 200

    except mysql.connector.Error:

        app.logger.exception("Unable to complete task")

        return jsonify({
            "error": "Unable to complete replenishment task."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:

            if connection.in_transaction:
                connection.rollback()

            connection.close()

# Retrieve stock movement history

@app.route("/api/stock-movements", methods=["GET"])
def get_stock_movements():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

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

        for movement in movements:

            movement["created_at"] = movement["created_at"].isoformat()

        return jsonify(movements), 200

    except mysql.connector.Error:

        app.logger.exception("Unable to retrieve stock movements")

        return jsonify({
            "error": "Unable to retrieve stock movement history."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

# Process inventory control transactions

@app.route("/api/inventory/<int:product_id>", methods=["PATCH"])
def update_inventory(product_id):

    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({"error": "Invalid request."}), 400

    action = data.get("action")
    quantity = data.get("quantity")
    username = data.get("username")
    reason = data.get("reason")

    # Validate transaction information

    if action not in ["receive", "damage", "reconcile", "shelf"]:

        return jsonify({
            "error": "Invalid transaction type."
        }), 400

    if type(quantity) is not int or quantity < 0:

        return jsonify({
            "error": "Invalid stock quantity."
        }), 400

    if action in ["receive", "damage"] and quantity == 0:

        return jsonify({
            "error": "Quantity must be greater than zero."
        }), 400

    if not isinstance(reason, str) or not reason.strip():

        return jsonify({
            "error": "A transaction reason is required."
        }), 400

    if len(reason.strip()) > 255:

        return jsonify({
            "error": "Reason cannot exceed 255 characters."
        }), 400

    if not isinstance(username, str) or not username.strip():

        return jsonify({
            "error": "Please select a user."
        }), 400

    try:

        connection = get_db_connection()

        connection.start_transaction()

        cursor = connection.cursor(dictionary=True)

        # Retrieve and lock current inventory record

        cursor.execute("""
            SELECT receiving_qty, shelf_qty
            FROM inventory
            WHERE product_id = %s
            FOR UPDATE
        """, (product_id,))

        inventory = cursor.fetchone()

        if inventory is None:

            return jsonify({
                "error": "Product not found."
            }), 404

        # Identify the user performing the transaction

        cursor.execute("""
            SELECT user_id
            FROM users
            WHERE username = %s
        """, (username,))

        user = cursor.fetchone()

        if user is None:

            return jsonify({
                "error": "User not found."
            }), 404

        receiving_before = inventory["receiving_qty"]
        shelf_before = inventory["shelf_qty"]

        receiving_after = receiving_before
        shelf_after = shelf_before

        # Receive supplier stock

        if action == "receive":

            receiving_after += quantity

            movement_type = "Stock Received"

        # Remove damaged stock

        elif action == "damage":

            if quantity > receiving_before:

                return jsonify({
                    "error": "Damaged quantity exceeds available stock."
                }), 400

            receiving_after -= quantity

            movement_type = "Damaged Stock"

        # Reconcile physical stock count

        elif action == "reconcile":

            receiving_after = quantity

            movement_type = "Stock Reconciliation"

        # Update actual shelf quantity

        elif action == "shelf":

            shelf_after = quantity

            movement_type = "Shelf Count Updated"

        if receiving_after > 2147483647 or shelf_after > 2147483647:

            return jsonify({
                "error": "Stock quantity is too large."
            }), 400

        # Update inventory quantities

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

        # Record stock movement

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
            reason.strip()
        ))

        connection.commit()

        return jsonify({
            "message": "Stock transaction recorded successfully.",
            "receiving_qty": receiving_after,
            "shelf_qty": shelf_after
        }), 200

    except mysql.connector.Error:

        app.logger.exception("Unable to update inventory")

        return jsonify({
            "error": "Unable to process inventory transaction."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:

            if connection.in_transaction:
                connection.rollback()

            connection.close()

# Retrieve system users from MySQL

@app.route("/api/users", methods=["GET"])
def get_users():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

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

    except mysql.connector.Error:

        app.logger.exception("Unable to retrieve users")

        return jsonify({
            "error": "Unable to retrieve system users."
        }), 500

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

# Run Flask application

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5001)