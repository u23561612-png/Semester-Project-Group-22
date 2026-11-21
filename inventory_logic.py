#inventoy logic behind the dashboard, to update stock levels etc
import math


def calculate_eoq (annual_demand, ordering_cost, holding_cost):
    
    #calculating economic order quantity using the EOQ formula
    if holding_cost <= 0 or annual_demand <= 0:
        return 0.0
    
    return math.sqrt( (2 * annual_demand * ordering_cost) / holding_cost)  #returning value


def calculate_quantity_needed (required_shelf_quantity, current_shelf_quantity):
    #calculating how many units are in need on the shop floor shelves
    
    quantity_needed = required_shelf_quantity - current_shelf_quantity
    
    return max( 0, quantity_needed )


def checking_stock_status(receiving_qty, quantity_needed):
    
    #this function determines the stock status for a product based on the receiving stock and 
    # the quantity needed. It returns one of three statuses: 'OUT OF STOCK', 'Sufficient', or 'Insufficient'.
   
    if receiving_qty == 0:
        return "OUT OF STOCK "
    
    elif receiving_qty >= quantity_needed:
        return "Sufficient "
    
    else:
        return "Insufficient "


def complete_replenishment_task(shelf_qty, required_shelf_qty,
                                receiving_qty, qty_to_move):
    """
    Moves stock from receiving to the shop floor
    while maintaining accurate inventory quantities.
    """

    if any(qty < 0 for qty in (
        shelf_qty, required_shelf_qty, receiving_qty
    )):
        raise ValueError("Stock quantities cannot be negative.")

    if qty_to_move <= 0:
        raise ValueError("Quantity to move must be positive.")

    quantity_needed = calculate_quantity_needed(
        required_shelf_qty, shelf_qty
    )

    if qty_to_move > receiving_qty:
        raise ValueError("Insufficient receiving stock.")

    if qty_to_move > quantity_needed:
        raise ValueError("Quantity exceeds shelf requirement.")

    new_shelf_qty = shelf_qty + qty_to_move

    new_receiving_qty = receiving_qty - qty_to_move

    out_of_stock_warning = None

    if new_receiving_qty == 0:
        out_of_stock_warning = (
            "WARNING: Item is now OUT OF STOCK in Receiving!"
        )

    return (
        new_shelf_qty,
        new_receiving_qty,
        out_of_stock_warning
    )


def reorder_supplier_stock (current_receiving_qty, reorder_amount):
    #function that adds stock coming from supplier to recieving area
    
    return current_receiving_qty + reorder_amount


def update_performance_stats(pending_tasks, completed_tasks, action="complete"):

    # Updating the pending and completed task metrics

    if action == "dispatch":
        pending_tasks += 1

    elif action == "complete":
        pending_tasks = max(0, pending_tasks - 1)
        completed_tasks += 1

    return pending_tasks, completed_tasks