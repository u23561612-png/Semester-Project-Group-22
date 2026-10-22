"""
Pick n Pay Wolmaransstad - Receiving Stock System Logic
Pure calculation and inventory state update functions.
"""

import math


def calculate_eoq(annual_demand, ordering_cost, holding_cost):
    """Calculates Economic Order Quantity (EOQ)[cite: 18]."""
    if holding_cost <= 0 or annual_demand <= 0:
        return 0.0
    return math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)


def calculate_quantity_needed(required_shelf_qty, current_shelf_qty):
    """Calculates how many units are needed on the shop floor shelf."""
    needed = required_shelf_qty - current_shelf_qty
    return max(0, needed)


def check_stock_status(receiving_qty, quantity_needed):
    """
    Determines stock status for a product based on receiving stock.
    Returns: 'OUT OF STOCK', 'Sufficient', or 'Insufficient'
    """
    if receiving_qty == 0:
        return "OUT OF STOCK"
    elif receiving_qty >= quantity_needed:
        return "Sufficient"
    else:
        return "Insufficient"


def complete_replenishment_task(shelf_qty, required_shelf_qty, receiving_qty, qty_to_move):
    """
    Simulates completing a replenishment task:
    1. Moves inventory from receiving to shelf.
    2. Deducts quantity from receiving stock.
    3. Returns updated values and out-of-stock warning message if receiving reaches 0.
    """
    # Restock shelf
    new_shelf_qty = min(required_shelf_qty, shelf_qty + qty_to_move)
    
    # Deduct from receiving stock
    new_receiving_qty = max(0, receiving_qty - qty_to_move)
    
    # Check for out-of-stock trigger
    out_of_stock_warning = None
    if new_receiving_qty == 0:
        out_of_stock_warning = "WARNING: Item is now OUT OF STOCK in Receiving! Please place a reorder."
        
    return new_shelf_qty, new_receiving_qty, out_of_stock_warning


def reorder_supplier_stock(current_receiving_qty, reorder_amount):
    """Adds incoming supplier stock to the receiving area."""
    return current_receiving_qty + reorder_amount


def update_performance_stats(pending_tasks, completed_tasks, action="complete"):
    """Updates pending and completed task metrics."""
    if action == "dispatch":
        pending_tasks += 1
    elif action == "complete":
        pending_tasks = max(0, pending_tasks - 1)
        completed_tasks += 1
        
    return pending_tasks, completed_tasks