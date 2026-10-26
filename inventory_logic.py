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


def complete_replenishment_task(shelf_qty, required_shelf_qty, receiving_qty, qty_to_move):
    #the logic behinfd the replenishment task, moving stock from receiving to shelf and deducting from receiving stock
    
    #1. Moves inventory from receiving to shelf.
    #2. Deducts quantity from receiving stock.
    #3. Returns updated values and out-of-stock warning message if receiving reaches 0.
   
    # Restocking shelf
    new_shelf_qty = min(required_shelf_qty, shelf_qty + qty_to_move)
    
    # Deducting from receiving stock
    new_receiving_qty = max(0, receiving_qty - qty_to_move)
    
    # Check for out of stock trigger
    out_of_stock_warning = None
    if new_receiving_qty == 0:
        out_of_stock_warning = " WARNING: Item is now OUT OF STOCK in Receiving, please place a reorder. "
        
    return new_shelf_qty, new_receiving_qty, out_of_stock_warning


def reorder_supplier_stock (current_receiving_qty, reorder_amount):
    #function that adds stock coming from supplier to recieving area
    
    return current_receiving_qty + reorder_amount


def update_performance_stats(pending_tasks, completed_tasks, action=" complete "):
    #function doing the logic behind the performance tab, updating the tasks completed as well as pending tasks
    
    if action == " dispatch":
        pending_tasks += 1 #incrementing pending tasks
        
    elif action == "complete ":
        pending_tasks = max(0, pending_tasks - 1)
        completed_tasks += 1    #incrementing completed tasks
        
    return pending_tasks, completed_tasks #returning the value calculated